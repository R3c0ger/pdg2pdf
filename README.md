# pdg2pdf

This is a simple CLI script to convert a series of PDG files to a single PDF file. 
本脚本用于将一系列 PDG 文件转换为单个 PDF 文件。

## Usage

usage: `pdg2pdf.py [-h] [--path PATH] [--output OUTPUT] [--del_exif]`

optional arguments:

| Arguments               | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `-h`, `--help`          | show this help message and exit                              |
| `--path`, `-p` PATH     | a path with target .pdg files inside <br />(default: the folder where this script is located) |
| `--output`, `-o` OUTPUT | the name of output .pdf file (default: output.pdf)           |
| `--del_exif`, `-d`      | delete the EXIF data from the .jpg file                      |

Example: 

`python pdg2pdf.py -p "C:/Users/xxx/Desktop/book" -o "book.pdf" -d`

Before running the script, renamimg .pdg files in a sequence is recommended.
在运行本脚本之前，建议将 .pdg 文件按顺序重命名。