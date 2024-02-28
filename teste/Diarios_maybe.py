import multiprocessing
import atexit
# from pythonProject.teste.login_sc_function import a as lsc
from pythonProject.teste.run_fake_br import run_daily_fk_br as run
from pythonProject.teste.succlele import run as sucmain


def cleanup_processes():
    if br and br.is_alive():
        br.terminate()
    if suc and suc.is_alive():
        suc.terminate()


if __name__ == '__main__':
    multiprocessing.freeze_support()  # Freezes support for multiprocessing // run as standalone instead
    atexit.register(cleanup_processes)


    print('rodando fake_br')
    br = multiprocessing.Process(target=run)
    br.start()

    print('rodando succlele')
    suc = multiprocessing.Process(target=sucmain)
    suc.start()
