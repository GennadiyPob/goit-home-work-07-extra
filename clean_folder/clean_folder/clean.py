import shutil
import sys
from pathlib import Path
import re #модуль регулярних обчислень

#обробка файлів. Path - збережений шлях до файлу: WindowsPath('tmp/Chess_position_from_black_side.jpg')
# root_folder - папка tmp
# dist - папка куди слід занести інформацію (перенести файли) 

'''БЛОК 1 - зміна імені файлів з кирилиці на латиницю'''

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}  #створюємо словник

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):  #ітеруємось: звертання до ключів і значень словника 
    TRANS[ord(key)] = value                             #створення (заповнення) словника TRANS
    TRANS[ord(key.upper())] = value.upper()             #створення (заповнення) словника TRANS великими буквами
    #словник TRANS заповнений малими і великими літерми

def normalize(name):                                #приймає на вхід ім'я файлу та переводить його в нове ім'я new_name
    name,*extension = name.split('.')              #розбиває ім'я файла на дві складові: ім'я та розширення
    new_name = name.translate(TRANS)                #заміна кириличних символів в імені файла
    new_name = re.sub(r'\W', '-', new_name)         #заміна не букв в імені файлу: дужки, пробіли, мінуси і т.д.
    return f"{new_name}.{'.'.join(extension)}"


'''БЛОК 2 - Сканування файлів і папок'''
'''створюємо списки відповідно до розширення файлів'''
jpeg_files = list()
doc_files = list()
video_files = list()
music_files = list()
folders = list()
archives = list()
others = list()
unknown = set()           #колекція НЕвідомих розширень  
extensions = set()        #колекція відомих розширень  

#словник, в якому ключі - розширення файлів
registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": jpeg_files,
    "JPG": jpeg_files,
    "SVG": jpeg_files,
    "TXT": doc_files,
    "DOCX": doc_files,
    "DOC": doc_files,
    "XLSX": doc_files,
    "PPTX": doc_files,
    "PDF": doc_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "MP3": music_files,
    "OGG": music_files,
    "WAV": music_files,
    "AMR": music_files,
    "ZIP": archives,
    "GZ": archives,
    "RAR": archives,
    "TAR": archives
}

#ф-ція обробки розширень
def get_extensions(file_name):                  #отримуємо ім'я файлу
    return Path(file_name).suffix[1:].upper()   #працюємо з суфіксом (беремо розширення) файлу  

'''сканування папок'''
def scan(folder):
    for item in folder.iterdir():                #проходимо по всім елементам папки
        if item.is_dir():                        #перевірка чи є елемент папцкою
            if item.name not in ('IMAGES' , 'DOCUMENTS', 'AUDIO', 'VIDEO', 'ARCHIVES'):  #ігноруємо папки для відсортованих файлів
                folders.append(item)             #додаємо назву пройденого каталогу в список
                scan(item)                       #скануємо папку                   
            continue                             #якщо папка зі списку то пропускаємо її

        #блок роботи з файлами  
        extension = get_extensions(file_name=item.name)  #працюємо з розширенням (відділяємо)

        new_name = folder / item.name                    #new_name - шлях. Передаємо шлях до файлу  

        if not extension:                                #перевіряємо чи є у файла розширення
            others.append(new_name)                      #додаємо його в список 'OTHERS'
        
        else:                                            #працюємо з файлами з розширеннями
            try:
                container = registered_extensions[extension]
                extensions.add(extension)                 #зберігаємо відомі розширення в множину (set)
                container.append(new_name)                #додаємо в контейнер ім'я файлу
            except KeyError:                              #KeyError якщо розширення не знайдено  
                unknown.add(extension)                    #зберігаємо НЕвідомі розширення
                others.append(new_name)                   #зберігаємо файли без розширень




    #друкуємо те що зберегли в контейнерах
    print(f'IMAGES jpeg, jpg, png, svg: {jpeg_files}\n')    
    print(f'VIDEO mp4, avi, mov, mkv : {video_files}\n')
    print(f'DOCS docs, doc, txt, xlsx, pptx, pdf : {doc_files}\n')
    print(f'MUSIC mp3, ogg, wav, amr: {music_files}\n')
    print(f'ARCHIVES zip, gz, rar: {archives}\n')
    print(f'others: {others}\n')
    print(f'All extensions: {extensions}')
    print(f'unknown extentions: {unknown}\n')


#обробка файлів

def hande_file(path, root_folder, dist):                         
    target_folder = root_folder / dist                           #Директорія з адресою, куди слід занести інформацію 
    target_folder.mkdir(exist_ok=True)                           #Створення директорії, якщо вона не існує.  
    path.replace(target_folder/normalize(path.name))   #перенесення файлів в потрібну директорію з оновленням імені


#обробка архівів

def handle_archive(path, root_folder, dist):                     #обробка архівів
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))  #зміна імені файлової директорії, прибераємо розширення zip

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), archive_folder)  #розпаковка архівних файлів
    except shutil.ReadError:                                             #розпаковка архівних файлів
        archive_folder.rmdir()
        return
    except FileNotFoundError:                                            #розпаковка архівних файлів
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):                                          #видалення пустих папок
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def get_folder_objects(root_path):                                      #перевірка елементів в папках
    for folder in root_path.iterdir():                                  #проходження по папкам
        if folder.is_dir():                                             #вхід якщо елемент папка
            remove_empty_folders(folder)                                #викликаємо функцію перевірки і видалення пустої папки
            try:
                folder.rmdir()
            except OSError:
                pass
      

def main(folder_path):
    scan(folder_path)
    remove_empty_folders(folder_path) 
    
    for file in jpeg_files:                    # проходимо по списку файлів зображень
        hande_file(file, folder_path, "IMAGES")     # записуємо file за адресою folder_path в папку IMAGES

    for file in doc_files:
        hande_file(file, folder_path, "DOCUMENTS")

    for file in video_files:
        hande_file(file, folder_path, "VIDEO")

    for file in music_files:
        hande_file(file, folder_path, "AUDIO")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVES")
    
       
    get_folder_objects(folder_path)


path = sys.argv[1]                                    #запуск через термінал, [1] - ім'я директорії 
arg = Path(path)   



#if __name__ == '__main__':
main(arg.resolve())
