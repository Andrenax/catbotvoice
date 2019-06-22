import speech_recognition as sr
from pydub import AudioSegment
from deeppavlov import build_model, configs
import os,sys
import argparse
import pandas as pd

#ledo a pasta inicial dos áudios
intencao = "obrigacao"
folder = 'C:\\Projetos\\Campus\\Audios\\'+intencao
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.tmp', '.m4a')
       output = os.rename(infilename, newname)

# Convert m4a extension files to wav extension files

formats_to_convert = ['.m4a']
lista = []
print("Extraíndo Texto...")
try:
    os.mkdir(folder+"_wav\\")
except OSError:  
    print ("Creation of the directory %s failed" % folder+"_wav\\")

for (dirpath, dirnames, filenames) in os.walk(folder):
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):

            filepath = dirpath + '\\' + filename
            (path, file_extension) = os.path.splitext(filepath)
            file_extension_final = file_extension.replace('.', '')
            
            #print(filepath)
            #print(file_extension_final)
            track = AudioSegment.from_file(filepath,
                    file_extension_final)
            
            wav_filename = filename.replace(file_extension_final, 'wav')

            r = sr.Recognizer() 

            wav_path = folder+"_wav\\"+wav_filename
            file_handle = track.export(wav_path, format='wav')
            with sr.WavFile(wav_path) as source: # use "test.wav" as the audio source
                audio = r.record(source) # extract audio data from the file 
                try:
                    #print()
                    #model = build_model(configs.morpho_tagger.UD2_0.morpho_ru_syntagrus_pymorphy, download=True)
                    lista.append(r.recognize_google(audio,language='pt-BR'))
                   
                    #print(lista)
                    #print("Arquivos de voz "+wav_filename+" Texto extraído: " + r.recognize_google(audio,language='pt-BR'))
                except LookupError: # speech is unintelligible
                    print("Could not understand audio")
df = pd.DataFrame(lista)
print(df.head().T)
print("Removendo os arquivos wav ...")
export_csv = df.to_csv (r'export_dataframe_'+intencao+'.csv', encoding="utf-8", index = None, header=False) #Don't forget to add '.csv' at the end of the path
