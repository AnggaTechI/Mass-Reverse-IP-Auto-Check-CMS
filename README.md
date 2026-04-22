<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=260&section=header&text=Mass%20Reverse%20IP%20Auto%20Check%20CMS&fontSize=34&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=High-performance%20reverse%20IP%20scanner%20with%20optional%20Auto%20Check%20CMS&descAlignY=58&descSize=16" width="100%" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=2500&pause=900&color=58A6FF&center=true&vCenter=true&repeat=true&width=950&lines=Mass+Reverse+IP+Auto+Check+CMS;Fast+Async+Reverse+IP+Scanner;Optional+Auto+Check+CMS;WordPress+%7C+Joomla+%7C+Drupal+%7C+Laravel+and+more;Built+by+AnggaTechI" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://github.com/AnggaTechI">
    <img src="https://img.shields.io/badge/GitHub-AnggaTechI-0d1117?style=for-the-badge&logo=github" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AsyncIO-High%20Performance-6A5ACD?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AIOHTTP-Fast-1E90FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Auto%20Check%20CMS-Enabled-EA4C89?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-00C853?style=for-the-badge" />
</p>

---

# Mass Reverse IP Auto Check CMS

> **High-performance reverse IP scanner with optional Auto Check CMS for WordPress, Joomla, Drupal, Laravel, and more.**

## Overview

**Mass Reverse IP Auto Check CMS** is a fast terminal-based Python tool for processing mixed targets such as **IP addresses, domains, and URLs**, then performing **reverse IP lookup** and optionally continuing with **Auto Check CMS** detection. The current script supports async lookup workers, optional CMS workers, per-CMS output files, mixed input normalization, and live terminal progress rendering.

Built for speed and clean terminal output, this tool helps you collect discovered domains quickly and optionally separate them into CMS-based result files for faster review.

---

## Features

- Fast **async reverse IP lookup**
- Accepts **IP / domain / URL** targets in one file
- Optional **Auto Check CMS** after reverse IP lookup
- Writes all unique discovered domains to `results.txt`
- Separate per-CMS output files
- Live terminal progress with lookup, IP, domain, and CMS counters
- Windows and Linux support
- Input and result de-duplication
- Clean terminal UI with colored banner and summary output

---

## Supported CMS

<p align="center">
  <img src="https://img.shields.io/badge/WordPress-21759B?style=for-the-badge&logo=wordpress&logoColor=white" />
  <img src="https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white" />
  <img src="https://img.shields.io/badge/Joomla-5091CD?style=for-the-badge&logo=joomla&logoColor=white" />
  <img src="https://img.shields.io/badge/Drupal-0678BE?style=for-the-badge&logo=drupal&logoColor=white" />
  <img src="https://img.shields.io/badge/Magento-EE672F?style=for-the-badge&logo=magento&logoColor=white" />
  <img src="https://img.shields.io/badge/Shopify-95BF47?style=for-the-badge&logo=shopify&logoColor=white" />
  <img src="https://img.shields.io/badge/CodeIgniter-EF4223?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PrestaShop-DF0067?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenCart-0E77B7?style=for-the-badge" />
  <img src="https://img.shields.io/badge/vBulletin-2D3E50?style=for-the-badge" />
  <img src="https://img.shields.io/badge/phpBB-4C5D7A?style=for-the-badge" />
</p>

---

## How It Works

```mermaid
flowchart TD
    A[input.txt] --> B[Normalize and dedupe targets]
    B --> C[Resolve host to IP]
    C --> D[Reverse IP lookup]
    D --> E[Write results.txt]
    E --> F{Auto Check CMS enabled?}
    F -- Yes --> G[Process discovered domains]
    G --> H[Detect CMS signatures]
    H --> I[Write per CMS files]
    F -- No --> J[Finish]
```

---

## Installation

Install dependencies:

```bash
python -m pip install aiohttp aiodns
```

Run the tool:

```bash
python main.py
```

---

## Usage

When the script starts, it will ask for:

- **Input file**
- **Enable Auto Check CMS?**
- **Concurrency value**

### Example input file

```txt
1.1.1.1
8.8.8.8
example.com
https://target.tld/path
sub.target.tld
```

---

## Output Files

### Main Output

```txt
results.txt
```

### CMS Output

```txt
wordpress.txt
laravel.txt
joomla.txt
drupal.txt
magento.txt
shopify.txt
codeigniter.txt
prestashop.txt
opencart.txt
vbulletin.txt
phpbb.txt
```

---

## Performance

- Async worker-based processing
- Separate reverse IP and Auto Check CMS stages
- Optimized defaults for Windows and Linux
- Fast DNS resolution path depending on platform
- Live progress updates during execution

---

## Terminal Preview

```text
[INPUT]
› File input  : targets.txt
› Active CMS detection? (Y/n) : y
› Concurrency (default=200, max=2000) : 200

▸ Total target  : 10,000
▸ Mode          : Reverse IP + Auto Check CMS
▸ Concurrency   : 200 (lookup) + 400 (cms)
▸ Output all    : results.txt
```

---

## Why This Tool

- Fast processing for large target lists
- Clean output separation by CMS
- Easy terminal workflow
- Good balance between speed and readable output
- Simple setup and direct execution

---

## Notes

- Reverse IP results depend on the upstream API response.
- Auto Check CMS is signature-based, so custom or heavily modified sites may appear as unknown.
- Use this tool only on infrastructure you manage or are authorized to assess.

---

## Author

<p align="center">
  <a href="https://github.com/AnggaTechI">
    <img src="https://github-readme-stats.vercel.app/api?username=AnggaTechI&show_icons=true&theme=tokyonight&hide_border=true" />
  </a>
</p>

<p align="center">
  <b>AnggaTechI</b><br>
  <a href="https://github.com/AnggaTechI">github.com/AnggaTechI</a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=120&section=footer" width="100%" />
</p>
