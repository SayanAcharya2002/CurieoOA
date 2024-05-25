FROM python
WORKDIR /solution
copy . /solution
CMD ["python","main.py"]