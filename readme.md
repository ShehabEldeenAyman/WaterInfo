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
