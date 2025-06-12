# Temperature Converter

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

if __name__ == '__main__':
    temp_c = float(input('Enter temperature in Celsius: '))
    temp_f = celsius_to_fahrenheit(temp_c)
    print(f'{temp_c}°C is {temp_f}°F')

    temp_f = float(input('Enter temperature in Fahrenheit: '))
    temp_c = fahrenheit_to_celsius(temp_f)
    print(f'{temp_f}°F is {temp_c}°C')
