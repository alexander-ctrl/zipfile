
if __name__ == "__main__":
    try:
        import PyQt5
        import zipfile
        import compressor
        from compressor import main

        main.startApp()

    except Exception as e:
        print(e)