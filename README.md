# confgrep
A grep tool for the top conferences, fork from https://github.com/Kyle-Kyle/top4grep

## Installation
```
git clone https://github.com/Yiteng-Peng/confgrep.git
cd confgrep
pip3 install -e .
```

## Usage 
### Database Initialization
If you want to update the papers stored in `papers.db`, you can recreate it with:
```bash
confgrep --build-db
```

Which will build the db wherever you run it.

```bash
confgrep --build-db -f <fields> -yl 2000 -yh 2024
```

Use `-yl` and `-yh` to set year low(default:2000) and year high(default:2024) 

Use `-f` to choose specific field, default is all field. Now support:
```python
CONFERENCES["SC"] = ["NDSS", "IEEE S&P", "USENIX", "CCS"]
CONFERENCES["SE"] = ["FSE", "ICSE", "ISSTA", "ASE"]
```
So you can use `-f sc` (case insensitive, so also fine for `-f SC`)
to only choose security conferences.

**Add your favorite conferences follow the comments in ./confgrep/config.py**

### Query
```bash
confgrep -k <kerywords>
```

For example, `python confgrep.py -k linux,kernel`
Currently, the query is just a case-insensitive match (just like grep). The returned results must contains all the input keywords (papers containing keyword1 AND keyword2 AND ...). Support for `OR` operation (papers containing keyword1 OR keyword2) is missing, but will be added in the future.

```bash
confgrep -k <kerywords> -f <fields> -yl 2000 -yh 2024
```

Use `-yl` and `-yh` to set year low(default:2000) and year high(default:2024) 

Use `-f` to choose specific field, default is all field. 

## Screenshot
![screenshot](./img/screenshot.png)

## TODO
- [ ] grep in abstract
- [ ] fuzzy match
- [ ] complex search logic (`OR` operation)