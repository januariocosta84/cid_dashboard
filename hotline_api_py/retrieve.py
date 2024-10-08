import os
def extract_origdate_with_wav_paths(directory):
    origdate_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                for line in file:
                    # Look for the line containing 'origdate'
                    if line.startswith("origdate="):
                        # Extract the origdate value
                        origdate = line.split('=', 1)[1].strip()
                        # Replace .txt with .wav in the filename
                        wav_filepath = filepath.replace(".txt", ".wav")
                        origdate_list.append((wav_filepath, origdate))
                        break  # Stop reading the file once origdate is found

    return origdate_list
directory = "C:\\Users\\TGA\OneDrive - IBI\\Desktop\\hotline_api_py\\new_voicemail"  #  folder path
dates = extract_origdate_with_wav_paths(directory)
for wav_filepath, date in dates:
    print(f"{wav_filepath}: {date}")


