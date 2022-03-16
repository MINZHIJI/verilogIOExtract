import logging

if __name__ == '__main__':
 
    # 基礎設定
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
    
    # 定義 handler 輸出 sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 設定輸出格式
    formatter = logging.Formatter('(%(levelname)6s)[%(name)10s]%(filename)16s:%(lineno)3d %(message)s')
    # handler 設定輸出格式
    console.setFormatter(formatter)
    # 加入 hander 到 root logger
    logging.getLogger('').addHandler(console)
    logging.info("[INFO] This is a main function for FSM auto generation")

