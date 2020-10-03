import sys   
import PySimpleGUI as sg
import serial as MyRS232
import time
# import serial.tools.list_ports
import RPi.GPIO as GPIO
# https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/tree/master/ADCDACPi
from ADCDACPi import ADCDACPi

def SendCde(CdeBase):
  if ser.isOpen():

    try:
        ser.flushInput() # flush input buffer, discarding all its contents
        ser.flushOutput()# flush output buffer, aborting current output 
                 # and discard all that is in buffer
        print(CdeBase)
        ser.write(CdeBase)
        time.sleep(0.1)  # give the serial port sometime to receive the data        
        response = ser.readline()
        print(response)
        window.Element('_OUTPUT_').Update(response)

    except IOError:
        print('No response...')

  else:
    print('cannot open serial port')
  return

layout = [[sg.Text('Retour des commandes bouton :'), sg.Text('', size=(30, 1), key='_OUTPUT_') ],  
          [sg.Button('Toggle led'), sg.Button('Read ADC')],
          [sg.InputText('9600', key = '_INBR_'), sg.Button('Baud Rate')],
          [sg.InputText('4', key = '_INPWR_'), sg.Button('Led Power')],
          [sg.InputText('0.4', key='_INCV_'), sg.Button('Set CVref')],
          [sg.InputText('Hello World', key = '_INSEND_'),
           sg.Text('Nombre d\'envois :'),sg.InputText('100', key = '_INCPT_'),
           sg.Button('Transmit')],
          [sg.Button('Exit')]]  

window = sg.Window('Window Title', layout)

ser = MyRS232.Serial(
    port="/dev/ttyAMA0",
    baudrate=9600,
    parity=MyRS232.PARITY_NONE,
    stopbits=MyRS232.STOPBITS_ONE,
    bytesize=MyRS232.EIGHTBITS
)
PTX1R = 25
PTX2R = 23
PTX3R = 22
PTX4R = 27

ser.isOpen()     
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # BCM numbering
GPIO.setup(17, GPIO.OUT) # LED
GPIO.setup(PTX1R, GPIO.OUT) # PTX1R
GPIO.setup(PTX2R, GPIO.OUT) # PTX2R
GPIO.setup(PTX3R, GPIO.OUT) # PTX3R
GPIO.setup(PTX4R, GPIO.OUT) # PTX4R

adcdac = ADCDACPi(1)     # gain DAC 1 ou 2
adcdac.set_adc_refvoltage(3.3)    # ref voltage 3.3 Volts
    
     #

while True:                 # event Loop  
  event, values = window.Read()  
  print(event, values)
#  print(values['_SLIDER_'])
  window.Element('_OUTPUT_').Update(event)
  if event is None or event == 'Exit':
      ser.close()
      break
  else:
      if event == 'Toggle led':    
          GPIO.output(17, not GPIO.input(17))     # toggle led
      if event == 'Read ADC':
          window.Element('_OUTPUT_').Update(adcdac.read_adc_voltage(1, 0))# read ADC channel 1 mode 1 (single ended)
      if event == 'Set CVref':
          CVref = values['_INCV_']
          print(CVref)
          adcdac.set_dac_voltage(1, float(CVref))    # set CVref channel 1, in Volts  
          window.Element('_OUTPUT_').Update('CVref set')
  
      if event == 'Baud Rate':
          ser.close
          ser.baudrate = int(values['_INBR_'])
          ser.isOpen()
          # change the "output" element to be the value of "input" element  
          window.Element('_OUTPUT_').Update('Baud rate set')         
      if event == 'Led Power':  
          GPIO.output(PTX1R, (0x01 & int(values['_INPWR_'])))
          GPIO.output(PTX2R, (0x02 & int(values['_INPWR_'])))
          GPIO.output(PTX3R, (0x04 & int(values['_INPWR_'])))
          GPIO.output(PTX4R, (0x08 & int(values['_INPWR_']))) 
          window.Element('_OUTPUT_').Update('Led power set')
      if event == 'Transmit':  
          CdeBase = str.encode(values['_INSEND_'])
          window.Element('_OUTPUT_').Update('')
          ser.timeout = 0.2
          TxLoop = int(values['_INCPT_'])
          while TxLoop > 0:
              SendCde(CdeBase)
              TxLoop -= 1
window.Close()




