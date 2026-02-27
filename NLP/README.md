启动封装好的fastapi接口

```
cd 文件目录
uvicorn main:app --host 127.0.0.1 --port 8000
```

输入网址:http://127.0.0.1:8000/docs可看到预测的界面

点击predict里的Trt it out在text里输入预测文本再点击Excute可看到Response body里的sentiment即预测结果