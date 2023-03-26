# fastapi_streamlit_test
fastapi_streamlit_test


### Build Setup in Windows

Only first time you need to do 

```
python -m venv .venv
.\.venv\Scripts\activate.ps1
python -m pip install -r ./requirements.txt
```


### Run 

```
.\.venv\Scripts\activate.ps1
python .\src\api_manager.py
```


### Docker run 

```
docker build -t streamlit-application .
docker run streamlit-application 
```
