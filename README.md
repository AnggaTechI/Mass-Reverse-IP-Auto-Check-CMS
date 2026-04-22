<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=280&section=header&text=Mass%20Reverse%20IP%20Auto%20Check%20CMS&fontSize=36&fontColor=ffffff&animation=twinkling&fontAlignY=38&desc=High-performance%20reverse%20IP%20scanner%20with%20optional%20Auto%20Check%20CMS%20for%20WordPress,%20Joomla,%20Drupal,%20Laravel,%20and%20more.&descAlignY=58&descSize=15" width="100%" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=2300&pause=700&color=FF3CAC&center=true&vCenter=true&repeat=true&width=1000&lines=Mass+Reverse+IP+Auto+Check+CMS;Fast.+Aggressive.+Async.;Reverse+IP+at+Scale;Auto+Check+CMS+for+Multi-Target+Workflows;Built+by+AnggaTechI" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://github.com/AnggaTechI"><img src="https://img.shields.io/badge/GitHub-AnggaTechI-0D1117?style=for-the-badge&logo=github" /></a>
  <img src="https://img.shields.io/badge/Python-3.x-111827?style=for-the-badge&logo=python&logoColor=FFD43B" />
  <img src="https://img.shields.io/badge/AsyncIO-Turbo-6D28D9?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AIOHTTP-Enabled-2563EB?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Auto%20Check%20CMS-Active-DB2777?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Terminal-Heavy%20Style-16A34A?style=for-the-badge" />
</p>

---

# ⚡ Mass Reverse IP Auto Check CMS

> ### High-performance reverse IP scanner with optional Auto Check CMS for WordPress, Joomla, Drupal, Laravel, and more.

---

## 🩸 What is this?

**Mass Reverse IP Auto Check CMS** is a high-speed terminal tool built to handle large target lists and keep output clean, organized, and easy to review.

Feed it **IPs, domains, or URLs**, let it rip through reverse IP collection, and when needed, continue directly into **Auto Check CMS** mode to sort discovered domains into platform-based result files.

This project is built around:

- **async reverse IP processing**
- **optional Auto Check CMS**
- **live terminal progress**
- **per-CMS output separation**
- **fast workflow for large batches**

---

## 🔥 Core Features

<table>
<tr>
<td width="50%">

### ⚔ Reverse IP Engine
- Fast async worker pipeline
- Mixed target support
- Input normalization
- Domain/IP de-duplication
- Large-list friendly flow

</td>
<td width="50%">

### 🧠 Auto Check CMS
- Optional CMS stage after reverse IP
- Per-CMS output split
- Quick signature-based detection
- Clean file separation
- Easy review workflow

</td>
</tr>
</table>

---

## 💀 Supported CMS

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
  <img src="https://img.shields.io/badge/vBulletin-1F2937?style=for-the-badge" />
  <img src="https://img.shields.io/badge/phpBB-475569?style=for-the-badge" />
</p>

---

## 🧨 Workflow

```mermaid
flowchart TD
    A[targets.txt] --> B[Normalize Targets]
    B --> C[Resolve Host to IP]
    C --> D[Reverse IP Lookup]
    D --> E[results.txt]
    E --> F{Auto Check CMS?}
    F -- Yes --> G[Analyze Discovered Domains]
    G --> H[Detect CMS Signatures]
    H --> I[Split Output by CMS]
    F -- No --> J[Done]
```

---

## 🚀 Installation

```bash
python -m pip install aiohttp aiodns
python main.py
```

---

## ⚙ Usage

When the tool runs, you will be prompted for:

- **input file**
- **Auto Check CMS mode**
- **concurrency value**

### Example input

```txt
1.1.1.1
8.8.8.8
example.com
https://target.tld/path
sub.target.tld
```

---

## 📂 Output Structure

### Main output

```txt
results.txt
```

### CMS output files

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

## 🖥 Terminal Style

This project is made to feel alive in the terminal:

- custom colored banner
- live counters
- progress rendering
- summary breakdown
- fast visual feedback during execution

---

## 🛡 Notes

- Reverse IP results depend on the upstream API response.
- Auto Check CMS is signature-based, so some targets may remain unknown.
- Use this tool only on infrastructure you manage or are authorized to assess.

---

## 👑 Author

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
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer" width="100%" />
</p>
