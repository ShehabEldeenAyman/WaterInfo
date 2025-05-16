# Waterinfo.be Use Case

This repository demonstrates the **Waterinfo.be** use case, designed to transform sensory data into a Linked Data Event Stream (LDES). The stream is made web-accessible, enabling easy fetching, storage, and querying.

---

## 🔍 What is Waterinfo Vlaanderen?

[Waterinfo Vlaanderen](https://www.waterinfo.be/) is the official online portal of the Flemish government for real-time water-related data and forecasts. Managed by the **Vlaamse Milieumaatschappij (VMM)**, it provides comprehensive information on:

- Water levels and tides
- Rainfall and droughts
- Flood risks throughout Flanders

### 🌊 Key Features

- **Real-Time Water Levels and Flood Forecasts**: Includes 48-hour flood predictions for rivers and streams.
- **Rainfall and Drought Monitoring**: Rain radar and pluviometer data.
- **Tide Information**: Tidal forecasts and digital tide books.
- **Flood Risk Maps**: Maps and watercourse data.

---

## 📥 Access to Data

There are two open-source libraries (Python and R) that facilitate access to Waterinfo data. These are maintained by **Fluves**, with contributions from **VITO**.

---

## 🔎 Data Overview

### Data Sources

- **VMM** (Vlaamse Milieumaatschappij)
- **HIC** (Hydrologisch Informatiecentrum)

### Sensor Data

- **Station info**: Location, address, etc.
- **Observations**: Timestamp, reading, units, etc.

### Challenges

- Discrete, unlinked readings
- No standard model (e.g., SSN/SOSA)
- Scattered data sources
- Difficult to compute on segmented data
- Large volumes = performance issues

---

## 🔧 Data Pipeline

### 1. Data Scraper

Fetches data from Waterinfo.be APIs (VMM/HIC). Each station and sensor has a unique ID. Up to 5 years of historical data can be fetched (with rate limits).

📌 **Standalone scraper module**: [GitHub Link](https://github.com/ShehabEldeenAyman/waterinfo-scrap)

#### Group List Attributes

- `group_id`
- `group_name`
- `group_type`

#### Station Attributes

Includes `ts_id`, `timestamp`, `station_latitude`, `station_name`, `ts_unitsymbol`, etc.

#### Sensor Reading Attributes

Includes `Value`, `QualityCode`, `Runoff Value`, `ReturnPeriod`, `Comment`, etc.

---

### 2. Data Pre-Processing

- Transforms attributes into **URI-compliant** format.
- Converts units to **UCUM** (Unified Code for Units of Measure).

---

### 3. Mapping Rules

Maps CSV readings to relational and semantic RDF using:

- **SSN/SOSA** ontologies
- **RML Mapper** & **RML Streamer**

---

### 4. Data Post-Processing

Optimizes RDF by:

- Replacing long URIs with prefixes.
- Reducing file size by up to **61%**.

📌 **Standalone prefix binder module**: [GitHub Link](https://github.com/ShehabEldeenAyman/rdf-prefix-binder)

---

### 5. Rules and Constraints

Applies validation via **SHACL shapes** to ensure model compliance.

---

### 6. LDES Conversion *(In Development)*

Converts RDF to LDES and adds **TREE hypermedia** for sensory observations.

> Future support will extend to general star-pattern observations.

---

## 📂 Output Formats

- **RDF-compliant data**
- **LDES data**

---

## 🧑‍💻 Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is licensed under the MIT License.


## 🚀 Getting Started

Follow the steps below to run the full Waterinfo data pipeline from scraping to LDES publishing.

---

### 📁 Directory Structure

- `waterinfo-scrap/` — Python module for scraping sensor data from waterinfo.be.
- `yarrrml/` — YARRRML mapping files for transforming CSV data to RML.
- `generated-rdf/` — Stores all intermediate and final RDF files.
- `Shacl-shapes/` — Contains SHACL shape definitions for validating RDF data.
- `data-postprocessing/` — Prefix handling script and configurations for RDF compression.
- `CommunitySolidServer/` — Local Solid Pod server for hosting RDF/LDES data.

---

### ⚙️ Step-by-Step Instructions

#### 1. Scrape Waterinfo Data

```bash
python waterinfo-scrap.py
```

Fetches raw sensor data from Waterinfo APIs and saves them in CSV format.

---

#### 2. Convert YARRRML to RML

```bash
yarrrml-parser -i yarrrml/timeseries.yml -o generated-rdf/timeseries.rml.ttl
```

Converts a YARRRML mapping into an RML-compliant Turtle file.

---

#### 3. Generate RDF with RMLMapper

```bash
java -jar rmlmapper.jar -m generated-rdf/yarrrml-mapping.rml.ttl -o generated-rdf/yarrrmlmapping.ttl

java -Xmx4g -jar rmlmapper.jar -m generated-rdf/timeseries.rml.ttl -o generated-rdf/timeseriesmapping.ttl
```

Transforms CSV data into RDF using RML mappings.

---

#### 4. Generate LDES with RMLStreamer

```bash
java -jar rmlstreamer.jar toFile -m generated-rdf/timeseries_ldes-mapping.rml.ttl -o generated-rdf/timeseriesmappingLDES.ttl
```

Converts RDF to an LDES-compatible format with TREE metadata.

---

#### 5. Validate with SHACL

```bash
pyshacl -s Shacl-shapes/shapes.ttl -d generated-rdf/timeseriesmapping.ttl
```

Validates RDF data using SHACL shapes to ensure model conformance.

---

#### 6. Prefix Optimization (Post-Processing)

```bash
python data-postprocessing/prefixSuffix.py \
  --graph generated-rdf/timeseriesmapping.ttl \
  --prefix data-postprocessing/prefixes/prefix.csv \
  --output generated-rdf/timeseries_with_prefixes.ttl
```

Compresses RDF file size by applying prefixes.

---

#### 7. Launch Solid Community Server (Optional for Hosting)

Install and run locally:

```bash
git clone https://github.com/CommunitySolidServer/CommunitySolidServer.git
cd CommunitySolidServer
npm ci
npm start
```

Or start a temporary server:

```bash
npx @solid/community-server
```

---

#### 8. Upload RDF to Solid Pod

```bash
curl -X POST \
  -H "Slug:waterinfo" \
  -H "Content-Type:text/turtle" \
  --data-binary "@timeseriesmapping.ttl" \
  http://localhost:3000/
```

Uploads RDF data to the running Solid Pod.

---

#### 9. (Optional) Run Penny UI

```bash
npm run dev
```

Launches the Penny UI (if used as an LDES interface).

---
