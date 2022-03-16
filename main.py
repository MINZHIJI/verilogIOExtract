import logging
import verilogIOExtract
import argparse
if __name__ == '__main__':
 
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('(%(levelname)6s)[%(name)10s]%(filename)16s:%(lineno)3d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("[INFO] This is a main function for module IO extracting")
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, required=True,  help='Input verilog file name')
    args = parser.parse_args()
    input_file = args.file
    vlogIOExtract = verilogIOExtract.verilogIOExtract()
    vlogIOExtract.parseModule(input_file)