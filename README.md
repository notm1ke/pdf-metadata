### pdf-metadata

A simple script that takes in a CSV file containing Accessibility information (see below for example) and exports a directory of metadata files.

#### Quick Start

In order to get started, ensure you have Python >=3.6 installed on your machine. Then clone this repository and install the `requirements.txt` file in case you do not have `pandas>=2.1.0` and/or `pyexiftool>=0.5.6` installed.

#### Usage

```
usage: pdf-metadata [-h] -i INPUT [-c]

Download PDFs from a source CSV file and extracts their metadata.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the source csv file
  -c, --clean           clean the csv file before processing
```

You must supply the input file using either the `-i` or `--input` flag. The `-c` or `--clean` flag is optional and will drop records that do not have a `Url` field in the source CSV file. It will save an additional file, named `clean.csv` and use that as the source CSV.

#### Output

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

The accessibility report CSV file typically has the following columns, however we only really care about the **Url** field in this script. Thus, you can basically assemble a CSV file of a bunch of URL rows and it will work just as well.

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

An example of a CSV file can be found in the `example` directory.