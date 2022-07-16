from pystrich.datamatrix import DataMatrixEncoder

encoder = DataMatrixEncoder("Hello")
print(encoder.get_ascii())
