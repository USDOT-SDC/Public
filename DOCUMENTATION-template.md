# \<Project Name> Data Documentation
* Project Acronym: \<PROJ-ACRNM>

## 1.0 Points of Contact (POCs)
Fill in the following, as appropriate and known
* **Project Owner:** Francis Sinatra, FSinatra@dot.gov
* **Management Lead:** Bobby Burns, BBurns@dot.gov
* **Evaluation Lead:** Ava Gardner, AGardner@mgm.com
* **Technical Lead:** Kenneth Rogers, KRogers@stevens.edu
* **Principal investigator(s):** 
* **Other Team Members:**
  * Dino Crocetti, DCrocetti@dot.gov
  * Sam Davis, SDavis@dot.gov

## 2.0 Dataset Overview:
* Introduction or abstract
* Time period covered by the data
* Physical location (description, polygon or lat/lon/elev) of observations in the dataset
* Data source if applicable
* Any website references (i.e. additional documentation such as Project website)

## 3.0 Instrument/Collection Device Description:

* Brief text (i.e. 1-2 paragraphs) describing the instrument(s) with references
* Figures (or links), if applicable
* Table of specifications (i.e. accuracy, precision, frequency, resolution, timezone, etc.)

## 4.0 Data Collection and Processing:

* Description of data collection
* Description of derived parameters and processing techniques used
* Description of quality control procedures
* Data intercomparisons, if applicable

## 5.0 Data Files:

* File names: Data file structure and file naming conventions (e.g. column delimited ASCII, NetCDF, GIF, JPEG, etc.)
* Field names: Data format and layout (i.e. description of header/data records,  sample records)
* Data type (i.e. string, int, ISO DATE/TIME, etc.)
* Description:
  * List of parameters with units, sampling intervals, frequency, range
  * Data version number and date
  * Description of flags, codes used in the data, and definitions (i.e. good, questionable, missing, estimated, etc.)

### 5.1 Data Elements

* File name
  * Field name [datatype] Description

### 5.2 Data Format Example

* agci_events_20210301.csv
  * event_datetime [ISO datetime] Date and time of event capture
  * event_id [int] Unique event identifier
  * event_type [string] Category of event
  * event_speed [decimal] Speed of vehicle in MPH

## 6.0 File Level Metadata

* If possible, file level metadata should be included at the beginning of ASCII text files
* If included, metadata will be enclosed in tags (\<metadata>\</metadata>)
* The contents of metadata will be in yaml format

### 6.1 Metadata Elements

If metadata is included, it should use the following elements.
* Required
  * PROJECT [string]
  * SUBSET, NAME [string]
  * SUBSET, FORMAT VERSION [decimal]
  * COUNT [integer]
* Optional
  * SUBSET, SOURCE [string]
  * COVERAGE, BEGIN [ISO DATE/TIME]
  * COVERAGE, END [ISO DATE/TIME]
  * REMARKS [string]
  * NOTIFY [email as string]

_*Please note that PROJECT and SUBSET, NAME values must be consistent throughout the SDC*_

_*See the next section for an example*_

### 6.3 Example
```
<metadata>
PROJECT: FRA-ARDS
SUBSET:
  NAME: AGCI
  FORMAT VERSION: 1.0
  SOURCE: RSIS [schema].[table_name]
COVERAGE:
  BEGIN: 2021-01-01T00:00:00.00-06:00
  END: 2021-01-31T00:00:00.00-06:00
COUNT: 142
REMARKS:
  - Office of Safety/Knowledge Management Division
  - Observation DATE/TIME provided in local timezone
  - No data available for 2021-01-16
NOTIFY:
  - KRogers@stevens.edu
  - DCrocetti@dot.gov
  - SDavis@dot.gov
</metadata>
DATE/TIME               LAT     LONG     ID        TYPE    TRESPASSER  FATALITY
                        Deg     Deg      NUMBER                        COUNT
2021-01-08T14:35-06:00  33.087  102.116  AI.20.1  Public   True        0
2021-01-15T05:48-06:00  33.090  102.120  AI.20.2  Private  False       0
2021-01-28T07:52-06:00  33.087  102.116  AI.20.3  Public   True        1
2021-01-30T18:16-06:00  33.090  102.120  AI.20.4  Private  False       0
```

## 7.0 Data Remarks:

* PI's assessment of the data (i.e. disclaimers, instrument problems, quality issues, etc.)
* Missing data periods
* Software compatibility (i.e. list of existing software to view/manipulate the data)

## 8.0 References:

* List of documents cited in this documentation
