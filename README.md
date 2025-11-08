# Beaver

Simple tool created to make log analysis easier.
Its principle task is to collect all IP addresses appearing in network traffic logs and then, using the ipinfo.io API, collect information about the ISP and country for further analysis.
<br>

## Usage

Before usage make sure you have all required libaries installed (requirements.txt) - you can use command below:

```
pip install -r requirements.txt

```

<br>Example usage:

```
python3 ./beaver.py <input_file>
```

## Switches:<br>

-d &lt;s&gt;, --delay &lt;s&gt;&nbsp;&nbsp;&nbsp;&nbsp;Delay between requests to avoid API rate limits (default: 0.5s)<br>
-f, --fast&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Skip entry banner (and it's delay)<br>
-p, --private&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Include private IPs in final file (idk why)<br>
<br>
At the end script provides 2 files:

1. TXT file containing list of all unique IPs found in logs
2. CSV file containing list of IPS with assigned ISP and Country
