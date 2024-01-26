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

### Query
```bash
confgrep -k <kerywords>
```

For example, `python confgrep.py -k linux,kernel`
Currently, the query is just a case-insensitive match (just like grep). The returned results must contains all the input keywords (papers containing keyword1 AND keyword2 AND ...). Support for `OR` operation (papers containing keyword1 OR keyword2) is missing, but will be added in the future.

## Screenshot
![screenshot](./img/screenshot.png)

## TODO
- [ ] support year filter and field filter for grep
- [ ] grep in abstract
- [ ] fuzzy match
- [ ] complex search logic (`OR` operation)