import argparse
import os
import platform
import sys
from pathlib import Path

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLO root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from yologui.yolo.yolov9.models.common import DetectMultiBackend
from yologui.yolo.yolov9.utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from yologui.yolo.yolov9.utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from yologui.yolo.yolov9.utils.plots import Annotator, colors, save_one_box
from yologui.yolo.yolov9.utils.torch_utils import select_device, smart_inference_mode

import shutil

from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QThread

def load_model(weights_path, device='', dnn=False, data=Path(ROOT / 'data/soybean2_1280pix/data.yaml'), half=False):
    device = select_device(device)
    model = DetectMultiBackend(weights_path, device=device, dnn=dnn, data=data, fp16=half)
    return model

class Detector(QThread):
    progressUpdated = Signal(int)
    # resultsReady = pyqtSignal(dict, dict, dict)
    
    def __init__(self, model_path):
        super().__init__()
        self.model = load_model(model_path)
        self.stop_requested = False

    @smart_inference_mode()
    def run(
            self, 
            weights=ROOT / 'yolo.pt',  # model path or triton URL
            source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
            data=ROOT / 'data/coco.yaml',  # dataset.yaml path
            imgsz=(640, 640),  # inference size (height, width)
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            view_img=False,  # show results
            save_txt=False,  # save results to *.txt
            save_conf=False,  # save confidences in --save-txt labels
            save_crop=False,  # save cropped prediction boxes
            nosave=False,  # do not save images/videos
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            visualize=False,  # visualize features
            update=False,  # update all models
            project=ROOT / 'runs/detect',  # save results to project/name
            name='exp',  # save results to project/name
            exist_ok=False,  # existing project/name ok, do not increment
            line_thickness=10,  # bounding box thickness (pixels)
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            half=False,  # use FP16 half-precision inference
            dnn=False,  # use OpenCV DNN for ONNX inference
            vid_stride=1,  # video frame-rate stride
    ):
        source = str(source)
        # save_img = not nosave and not source.endswith('.txt')  # save inference images
        save_img = not source.endswith('.txt')  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
        screenshot = source.lower().startswith('screen')
        if is_url and is_file:
            source = check_file(source)  # download

        # Directories
        save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Load model
        device = select_device(device)
        # model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
        stride, names, pt = self.model.stride, self.model.names, self.model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size

        # Dataloader
        bs = 1  # batch_size
        if webcam:
            view_img = check_imshow(warn=True)
            dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            bs = len(dataset)
        elif screenshot:
            dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        vid_path, vid_writer = [None] * bs, [None] * bs

        # Run inference
        self.model.warmup(imgsz=(1 if pt or self.model.triton else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        
        #返回值字典
        images_dict = {}  # 存储每个处理过的图片，键为图片路径，值为图片数据
        info_dict = {}  # 存储每张图片的检测信息，包括豆子总数、含裂纹豆子数等
        time_dict = {}  # 存储每张图片的处理时间
        
        for path, im, im0s, vid_cap, s in dataset:
            if self.stop_requested:
                print("detect is stopped")
                self.stop_requested = False
                return images_dict, info_dict, time_dict  # 返回空字典，表示被取消
            
            with dt[0]:
                im = torch.from_numpy(im).to(self.model.device)
                im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                pred = self.model(im, augment=augment, visualize=visualize)
                pred = pred[0][1]

            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)
            
            # 修改：过滤肯定超过尺寸的大框，打印最终检测数量
            cracked_class_index = 0
            # Process predictions
            for i, det in enumerate(pred):  # per image
                if det.size(0):  # 确认存在检测结果
                    max_size_threshold_w = 96
                    max_size_threshold_h = 96
                    # 过滤宽度
                    det_w_filtered = det[(det[:, 2] - det[:, 0]) <= max_size_threshold_w]
                    # 过滤高度
                    det_filtered = det_w_filtered[(det_w_filtered[:, 3] - det_w_filtered[:, 1]) <= max_size_threshold_h]
                    # 结果信息
                    cracked_count = (det_filtered[:, -1] == cracked_class_index).sum().item()
                    # 更新结果
                    pred[i] = det_filtered  # 更新当前图像的检测结果
                    # 我存
                    info_dict[path] = {"豆子总数": det_filtered.size(0), "含裂纹豆子数": cracked_count, "裂纹占比": cracked_count/det_filtered.size(0)}
                #结束修改
                
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string 宽度x高度
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det_filtered):
                    # Rescale boxes from img_size to im0 size
                    det_filtered[:, :4] = scale_boxes(im.shape[2:], det_filtered[:, :4], im0.shape).round()

                    # Print results
                    for c in det_filtered[:, 5].unique():
                        n = (det_filtered[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det_filtered):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            # 改-本系统：颜色、标签、粗细
                            if c == 0:  # 裂纹
                                color =  (20, 20, 225) #  深红
                                label = f'crack {conf:.2f}'
                            elif c == 1:  # 非裂纹
                                color = (175, 175, 95)   # 蓝
                                label = f'other {conf:.2f}'
                            else:
                                color = colors(c, True)  # 默认颜色
                            annotator.box_label(xyxy, label, color=color)
                            
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                # Stream results
                im0 = annotator.result()
                # 我存返回值
                images_dict[path] = im0
                if view_img: #默认值False，不会在这里显示图像
                    if platform.system() == 'Linux' and p not in windows:
                        windows.append(p)
                        cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                        cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image' and not nosave:
                        # 存！
                        cv2.imwrite(save_path, im0)
                    # else:  # 'video' or 'stream'
                    #     if vid_path[i] != save_path:  # new video
                    #         vid_path[i] = save_path
                    #         if isinstance(vid_writer[i], cv2.VideoWriter):
                    #             vid_writer[i].release()  # release previous video writer
                    #         if vid_cap:  # video
                    #             fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    #             w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    #             h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    #         else:  # stream
                    #             fps, w, h = 30, im0.shape[1], im0.shape[0]
                    #         save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                    #         vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    #     vid_writer[i].write(im0)

            # Print time (inference-only)
            LOGGER.info(f"{s}{'' if len(det_filtered) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
            # 我存返回值
            time_dict[path] = f"{dt[1].dt * 1E3:.1f}ms"
            
            parts = s.split()
            current_image, total_images = map(int, parts[1].split('/'))  # 直接从s解析当前图像编号和总数
            self.progressUpdated.emit(int((current_image / total_images) * 100))
        
        # Print results
        t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
        LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
        
        # 先不存--存
        if save_txt or (save_img and not nosave):
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
        if update:
            strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)
        
        # 删除目录
        if nosave:   
            shutil.rmtree(save_dir)
        
        # self.resultsReady.emit(images_dict, info_dict, time_dict)
        
        return images_dict, info_dict, time_dict

    def Detect_Soybean_Crack(
            self, 
            source,
            weights=[ROOT / 'My_Work_Place/weights/best5_1.pt'],
            data=ROOT / 'data/soybean2_1280pix/data.yaml',
            imgsz=[640],
            conf_thres=0.08,
            iou_thres=0.45,
            max_det=120,
            device='',
            view_img=False,
            save_txt=False,
            save_conf=False,
            save_crop=False,
            nosave=False, #False：保存图像
            classes=None,
            agnostic_nms=True,
            augment=False,
            visualize=False,
            update=False,
            project=ROOT / 'runs/detect', #保存路径
            name='exp',
            exist_ok=False,
            line_thickness=5,
            hide_labels=False,
            hide_conf=False,
            half=False,
            dnn=False,
            vid_stride=1,
        ):
        # 转换 imgsz 参数以匹配原始逻辑
        imgsz = imgsz * 2 if len(imgsz) == 1 else imgsz

        # 构建 opt 字典
        opt = {
            'weights': weights,
            'source': str(source),  # 确保路径被转换成字符串
            'data': str(data),
            'imgsz': imgsz,
            'conf_thres': conf_thres,
            'iou_thres': iou_thres,
            'max_det': max_det,
            'device': device,
            'view_img': view_img,
            'save_txt': save_txt,
            'save_conf': save_conf,
            'save_crop': save_crop,
            'nosave': nosave,
            'classes': classes,
            'agnostic_nms': agnostic_nms,
            'augment': augment,
            'visualize': visualize,
            'update': update,
            'project': str(project), 
            'name': name,
            'exist_ok': exist_ok,
            'line_thickness': line_thickness,
            'hide_labels': hide_labels,
            'hide_conf': hide_conf,
            'half': half,
            'dnn': dnn,
            'vid_stride': vid_stride,
        }

        # 调用 run 函数并接收返回值
        images_dict, info_dict, time_dict = self.run(**opt)
        
        # 返回这些字典
        return images_dict, info_dict, time_dict
