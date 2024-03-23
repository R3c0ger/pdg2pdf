#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import sys
import time

import jpg2pdf
from piexif import remove as rm_exif
from tqdm import tqdm


def argparser():
    """Get the target folder. \n获取目标文件夹"""
    # Get the current folder. 获取脚本所在的文件夹
    current_dir = os.getcwd()
    print(f"\nThe folder where this script is located: {current_dir}")

    # Parse the command-line arguments. 解析命令行参数
    parser = argparse.ArgumentParser(
        description='Convert .pdg files to .pdf file',
        epilog='Example: python pdg2pdf.py -p "C:/Users/xxx/Desktop/book" -o '
               '"book.pdf" -d Before running the script, renamimg .pdg files'
               ' in a sequence is recommended. 在运行本脚本之前，建议将 .pdg 文件'
               '按顺序重命名。',
    )
    parser.add_argument('--path', '-p',
                        type=str, default=os.getcwd(), required=False,
                        help="a path with target .pdg files inside (default:"
                             " the folder where this script is located)")
    parser.add_argument('--output', '-o',
                        type=str, default=None, required=False,
                        help="the name of output .pdf file "
                             "(default: output.pdf)")
    parser.add_argument('--del_exif', '-d',
                        action='store_true', required=False,
                        help="delete the EXIF data from the .jpg file")
    args = parser.parse_args()

    _path, _pdf_name, _del_exif_flag = args.path, args.output, args.del_exif
    print(f"The target folder: {_path}"
          f"\nDelete the EXIF data: {_del_exif_flag}")
    return _path, _pdf_name, _del_exif_flag

def check_dir(_path, _pdf_name):
    """Check if the folder exists. If exists, change the current folder.
    检查文件夹是否存在。如果存在，更改当前文件夹。"""
    if not os.path.exists(_path):
        print(f"Error: the folder '{_path}' does not exist.")
        sys.exit(1)
    if not os.path.isdir(_path):
        print(f"Error: '{_path}' is not a folder.")
        sys.exit(1)

    if _pdf_name is None:
        _pdf_name = os.path.basename(_path) + ".pdf"
    print(f"The name of output .pdf file: {_pdf_name}")
    os.chdir(_path)
    print(f"Changed the current folder to '{_path}'.")
    return _pdf_name

def get_pdg_files():
    """Get the list of .pdg files.\n获取 .pdg 文件列表"""
    _pdg_files = [f for f in os.listdir() if f.endswith(".pdg")]
    if not _pdg_files:
        print(f"Error: no .pdg files found in the folder '{os.getcwd()}'.")
        sys.exit(1)
    else:
        # print(f"\nList of .pdg files: {_pdg_files}")
        print(f"\nNumber of .pdg files: {len(_pdg_files)}")
    return _pdg_files

def make_jpg_folder():
    """Make a folder with a timestamp for the .jpg files.
    为 .jpg 文件创建一个带有时间戳的文件夹"""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        _jpg_folder = f"jpg_{timestamp}"
        os.makedirs(_jpg_folder)
        print(f"\nFolder name of converted .jpg files: {_jpg_folder}")
        return _jpg_folder
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def del_exif(_jpg_file):
    """Delete the EXIF data from the .jpg file.
    从 .jpg 文件中删除 EXIF 数据"""
    try:
        # image = Image.open(_jpg_file)
        # data = list(image.getdata())
        # image_without_exif = Image.new(image.mode, image.size)
        # image_without_exif.putdata(data)
        # image_without_exif.save(_jpg_file)
        # # The above code would make files larger. 上面的代码会使文件变大
        rm_exif(_jpg_file)  # 使用的是 piexif 库的 remove 函数
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def cvt_pdg2jpg(_pdg_files, _jpg_folder, _del_exif_flag=True):
    """Convert .pdg files to .jpg files.\n
    将 .pdg 文件转换为 .jpg 文件

    :param _pdg_files: list of .pdg files
    :param _jpg_folder: folder with .jpg files
    :param _del_exif_flag: delete the EXIF data from the .jpg file
    :return: None
    """
    try:
        print(f"\nConversion from PDG to JPG started...")
        pbar = tqdm(_pdg_files)
        for pdg_file in pbar:
            jpg_file = pdg_file.replace(".pdg", ".jpg")
            jpg_path = os.path.join(_jpg_folder, jpg_file)
            pbar.set_description(f"Processing {pdg_file}")
            shutil.copyfile(pdg_file, jpg_path)
            # Delete the EXIF data from the .jpg file.
            # 从 .jpg 文件中删除 EXIF 数据
            if _del_exif_flag:
                del_exif(jpg_path)
        print(f"Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def _extract_special_pages(_jpg_files, prefix):
    """Extract special pages from the .jpg files.
    从 .jpg 文件中提取特殊页面

    :param _jpg_files: list of .jpg files
    :param prefix: the prefix of the special .jpg files
    :return spc_list: list of special .jpg files
    :return _jpg_files: list of remaining .jpg files
    """
    spc_list = []
    for f in _jpg_files:
        if prefix in f:
            spc_list.append(f)
    for f in spc_list:
        _jpg_files.remove(f)
    return spc_list, _jpg_files

def reorder_pages(_jpg_files):
    """Reorder the pages of the .jpg files.
    重新排列 .jpg 文件的页面

    :param _jpg_files: list of .jpg files
    :return reordered_files: list of reordered .jpg files
    """
    # Extract special pages. 提取特殊页面
    cov, remain = _extract_special_pages(_jpg_files, "cov")
    cov_1, cov_other = cov[:1], cov[1:]
    bok, remain = _extract_special_pages(remain, "bok")
    leg, remain = _extract_special_pages(remain, "leg")
    fow, remain = _extract_special_pages(remain, "fow")
    # Reorder the pages. 重新排列页面
    # Follow the order: 封面(cov), 书名(bok), 版权页(leg), 前言(fow), 目录和正文, back cover
    reordered_files = cov_1 + bok + leg + fow + remain + cov_other
    return reordered_files

def cvt_jpg2pdf(_jpg_folder, _pdf_name):
    """Convert .jpg files to .pdf file.
    将 .jpg 文件转换为 .pdf 文件

    :param _jpg_folder: folder with .jpg files
    :param _pdf_name: the name of output .pdf file
    :return: None
    """
    # Get the list of .jpg files. 获取 .jpg 文件列表
    _jpg_files = [f for f in os.listdir(_jpg_folder) if f.endswith(".jpg")]
    if not _jpg_files:
        print(f"Error: no .jpg files found in the folder '{_jpg_folder}'.")
        sys.exit(1)
    # Reorder the pages. 重新排列页面
    _jpg_files = reorder_pages(_jpg_files)

    # Convert .jpg files to .pdf file. 将 .jpg 文件转换为 .pdf 文件
    with jpg2pdf.create(_pdf_name) as pdf:
        print(f"\nConversion from JPG to PDF started...")
        pbar = tqdm(_jpg_files)
        for jpg_file in pbar:
            pbar.set_description(f"Adding {jpg_file}")
            pdf.add(os.path.join(_jpg_folder, jpg_file))
        print(f"Done.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    # Parse the command-line arguments. 解析命令行参数
    path, pdf_name, del_exif_flag = argparser()
    # Check if the folder exists. 检查文件夹是否存在
    pdf_name = check_dir(path, pdf_name)
    # Get the list of .pdg files. 获取 .pdg 文件列表
    pdg_files = get_pdg_files()
    # Make a folder for the .jpg files. 为 .jpg 文件创建文件夹
    jpg_folder = make_jpg_folder()
    # Convert .pdg files to .jpg files. 将 .pdg 文件转换为 .jpg 文件
    cvt_pdg2jpg(pdg_files, jpg_folder, del_exif_flag)
    # Convert .jpg files to .pdf file. 将 .jpg 文件转换为 .pdf 文件
    cvt_jpg2pdf(jpg_folder, pdf_name)
    # Delete the folder with .jpg files. 删除带有 .jpg 文件的文件夹
    shutil.rmtree(jpg_folder)