# pdg2pdf

This is a simple CLI script to convert a series of PDG files to a single PDF file. 
本脚本用于将一系列 PDG 文件转换为单个 PDF 文件。

## Usage

usage: 
- `pdg2pdf.py [-h] [--path PATH] [--output OUTPUT] [--del_exif]`
- `pdg2pdf.exe [-h] [--path PATH] [--output OUTPUT] [--del_exif]`

optional arguments:

| Arguments               | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `-h`, `--help`          | show this help message and exit                              |
| `--path`, `-p` PATH     | a path with target .pdg files inside <br />(default: the folder where this script is located) |
| `--output`, `-o` OUTPUT | the name of output .pdf file (default: output.pdf)           |
| `--del_exif`, `-d`      | delete the EXIF data from the .jpg file                      |

Example: 

- `python pdg2pdf.py -p "C:/Users/xxx/Desktop/book" -o "book.pdf" -d`
- `pdg2pdf.exe -p "C:/Users/xxx/Desktop/book" -o "book.pdf" -d`

Before running the script, renamimg .pdg files in a sequence is recommended.
在运行本脚本之前，建议将 .pdg 文件按顺序重命名。

## Requirements

- Python 3.6+
- jpg2pdf~=0.1.0
- piexif~=1.1.3
- tqdm~=4.66.2

## Reference

- [超星图书馆书转化为PDF格式的方法](https://www.360docs.net/doc/b312672264.html)