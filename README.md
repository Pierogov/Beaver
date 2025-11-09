# Beaver
Simple tool created to make log analysis easier. Its principle task is to collect all IP addresses appearing in network traffic logs and then, using the ipinfo.io API, collect information about the ISP and country for further analysis.
<br><br>
![Beaver image](./img/beaver_banner.jpg)
## Usage

If anything doesn't work, please make sure you have all required libaries installed (requirements.txt) - you can use command below:

```
pip install -r requirements.txt
```

<br>Example usage (Search for all IPs in successful logins):

```
python3 ./beaver.py <input_file> -s "Pass"
```

## Switches:<br>
-s &lt;str&gt;,--success &lt;str&gt;&nbsp;&nbsp;&nbsp;If set, the program will only parse records with successfull login, searched by provided string.<br>
-d &lt;s&gt;, --delay &lt;s&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Delay between requests to avoid API rate limits (default: 0.5s)<br>
-f, --fast&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Skip unnecesary messages and banners made to look better<br>
-p, --private&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Include private IPs in final file (idk why)<br>
<br>
At the end script provides 2 files:

1. TXT file containing list of all unique IPs found in logs
2. CSV file containing list of IPS with assigned ISP and Country
