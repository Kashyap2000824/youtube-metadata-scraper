import pandas as pd
import yt_dlp

input_file = "video_urls.csv"
output_file = "yt_metadata_output.csv"

df = pd.read_csv(input_file)
urls = df.iloc[:, 0].dropna().tolist()

metadata = []

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'extract_flat': False,
    'forcejson': True
}

for url in urls:
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            data = {
                "Title": info.get("title", ""),
                "Channel": info.get("channel", ""),
                "Views": info.get("view_count", ""),
                "Duration (sec)": info.get("duration", ""),
                "Upload Date": info.get("upload_date", ""),
                "Description": info.get("description", "")[:200]
            }
            metadata.append(data)
    except Exception as e:
        metadata.append({
            "Title": "Error",
            "Channel": "Error",
            "Views": "Error",
            "Duration (sec)": "Error",
            "Upload Date": "Error",
            "Description": f"Error: {str(e)}"
        })

output_df = pd.DataFrame(metadata)
output_df.to_csv(output_file, index=False)

print(f"✅ Metadata saved to '{output_file}'")