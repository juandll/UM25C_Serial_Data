## Usage

Fist step is setting the device connectivity via Bluetooth and connecting it to a serial COM port. We need to identify the port that it is using. Afet this we execute:


```python main.py <COM Port> <Output CSV File> ```


This will create a csv file. If we would like to merge it with any other metrics such as system metrics, CPU, RAM and RX & TX we can execute the match script.


```python match.py <Power csv> <System csv> <Output csv>```


Lastly to plot this data we also provided a plot file that is executed as follow:


```python plot.py <Merged csv>```
