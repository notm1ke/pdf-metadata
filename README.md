### pdf-metadata

A simple script that takes in a CSV file containing Accessibility information (see below for example) and exports a directory of metadata files.

#### Quick Start

In order to get started, ensure you have Python >=3.6 installed on your machine. Then clone this repository and install the `requirements.txt` file in case you do not have `pandas>=2.1.0`, `pyexiftool>=0.5.6`, or `requests>=2.31.0` installed.

If you have problems installing the requirements file, you can install the packages manually using the following commands:

```bash
$ pip3 install pandas
$ pip3 install pyexiftool
$ pip3 install requests
```

#### Usage

```
usage: pdf-metadata [-h] -i INPUT [-m {json,csv}]

Download PDFs from a source CSV file and extracts their metadata.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the source csv file
  -m {json,csv}, --mode {json,csv}
                        mode to run the script in
```

##### Example

```bash
$ python3 pdf-metadata -i example/clean.csv
#                         ^ path to source csv file

$ python3 pdf-metadata -i example/clean.csv -m json
#                         ^ path to source csv file
#                                           ^ output metadata in JSON format
```

You must supply the input file using either the `-i` or `--input` flag. Additionally, you can supply the `-m` or `--mode` flag to specify the output format of the metadata files. The default is `csv` which will output a `metadata.csv` file in the root directory, but you can also use `json` which will generate a directory, `./pdfs/meta` that has a JSON file for each PDF file.

#### Output

##### CSV Format

Once ran, a `metadata.csv` file is created in the root directory of the project. This file will contain the following structure:

| Url                     | Title                    | Author                   | Creator                  | Producer                 | Version | Size  | Xmp                      | Pages |
|-------------------------|-------------------------|-------------------------|-------------------------|-------------------------|---------|-------|-------------------------|-------|
| https://draft-president.media.uconn.edu/wp-content/uploads/sites/3778/2024/01/1.-Protect-Our-Pack-Task-Force-Presentation.pdf | Protect Our Pack  Orientation  & other Training Programs | Longa, Jenn | Acrobat PDFMaker 20 for PowerPoint | Adobe PDF Library 20.5.106 | 1.6 | 204702 | Adobe XMP Core 5.6-c017 91.164464, 2020/06/15-10:20:05 | 10 |

##### JSON Format

Once ran, a `pdfs` folder is created in the root directory of the project. This has both all of the downloaded PDFs and the metadata, under a `meta` folder. Each metadata file corresponds with the name of it's respective PDF file, and will contain the following JSON payload:

```json
{
   "url": "https://draft-president.media.uconn.edu/wp-content/uploads/sites/3778/2024/01/1.-Protect-Our-Pack-Task-Force-Presentation.pdf",
   "title": "Protect Our Pack  Orientation  & other Training Programs",
   "author": "Longa, Jenn",
   "creator": "Acrobat PDFMaker 20 for PowerPoint",
   "producer": "Adobe PDF Library 20.5.106",
   "version": 1.6,
   "size": 204702,
   "xmp": "Adobe XMP Core 5.6-c017 91.164464, 2020/06/15-10:20:05        ",
   "pages": 10
}
```

The folder structure looks like this:

```
pdfs/
├── meta
│   ├── one.json
│   ├── ...
│   ├── n.json
├── one.pdf
├── ...
├── n.pdf
```

#### CSV format

The accessibility report CSV file typically has the following columns, however we only really care about the **Url**, **Mime type**, and **Deleted at** fields in this script. Thus, you can basically assemble a CSV file of a bunch of URL rows, Mime types, and blank deleted at fields and it will work just as well. This is simply the format the UConn reports tend to come in.

| Field                   |
|-------------------------|
| Id                      |
| Name                    |
| Mime type               |
| Score                   |
| Deleted at              |
| Library reference       |
| Url                     |
| Checked on              |
| AlternativeText:2       |
| Contrast:2              |
| HeadingsHigherLevel:3   |
| HeadingsPresence:2      |
| HeadingsSequential:3    |
| HeadingsStartAtOne:3    |
| HtmlBrokenLink:2        |
| HtmlCaption:2           |
| HtmlColorContrast:2     |
| HtmlDefinitionList:3    |
| HtmlEmptyHeading:2      |
| HtmlEmptyTableHeader:2  |
| HtmlHasLang:3           |
| HtmlHeadingOrder:3      |
| HtmlHeadingsPresence:2  |
| HtmlHeadingsStart:2     |
| HtmlImageAlt:2          |
| HtmlImageRedundantAlt:3 |
| HtmlLabel:2             |
| HtmlLinkName:3          |
| HtmlList:3              |
| HtmlObjectAlt:2         |
| HtmlTdHasHeader:2       |
| HtmlTitle:3             |
| ImageContrast:2         |
| ImageDecorative:2       |
| ImageDescription:2      |
| ImageOcr:3              |
| ImageSeizure:1          |
| LanguageCorrect:3       |
| LanguagePresence:3      |
| Ocred:2                 |
| Parseable:1             |
| Scanned:1               |
| Security:1              |
| TableHeaders:2          |
| Tagged:2                |
| Title:3                 |

Here is a sample line of the above format.

```csv
QzDB69ivWdlf3d9ifBKgUr3DgOjVxid9+beJg+bMmlA=,1.-Protect-Our-Pack-Task-Force-Presentation.pdf,application/pdf,0.5361625,,,https://draft-president.media.uconn.edu/wp-content/uploads/sites/3778/2024/01/1.-Protect-Our-Pack-Task-Force-Presentation.pdf,4/1/2022 20:16,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

An example of a valid [CSV file](./examples/source.csv) can be found under the `example` directory.