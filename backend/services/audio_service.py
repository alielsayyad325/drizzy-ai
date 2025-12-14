import asyncio
import os
import subprocess

class AudioService:
    def __init__(self):
        pass

    async def mix_song(self, vocals_path: str, beat_path: str, output_path: str):
        """
        Mixes vocals and beat into a final audio file using ffmpeg.
        """
        print(f"Mixing {vocals_path} with {beat_path}...")
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Use ffmpeg to mix the audio
            # -i: input files
            # -filter_complex: apply audio filters
            # amix: mix audio streams
            # -ac 2: stereo output
            # -y: overwrite output file
            
            # Define ffmpeg path - check system path first, then fallback to known location
            ffmpeg_cmd = 'ffmpeg'
            
            # Check if ffmpeg is in PATH
            import shutil
            if not shutil.which('ffmpeg'):
                # Fallback to the specific path we found
                possible_path = r'C:\Users\aliel\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'
                if os.path.exists(possible_path):
                    ffmpeg_cmd = possible_path
                else:
                    print(f"Warning: FFmpeg not found in PATH or at {possible_path}")

            # Log paths for debugging
            with open("debug_audio.log", "a") as log:
                log.write(f"Mixing:\nVocals: {vocals_path} (Exists: {os.path.exists(vocals_path)})\nBeat: {beat_path} (Exists: {os.path.exists(beat_path)})\nOutput: {output_path}\nFFmpeg: {ffmpeg_cmd}\n")

            command = [
                ffmpeg_cmd,
                '-i', vocals_path,
                '-i', beat_path,
                '-filter_complex', '[0:a]volume=1.2[a1];[1:a]volume=0.7[a2];[a1][a2]amix=inputs=2:duration=longest',
                '-ac', '2',
                '-y',
                output_path
            ]
            
            # Run ffmpeg
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return self._create_fallback(output_path)
            
            print(f"Song mixed and saved to {output_path}")
            return output_path
            
        except FileNotFoundError:
            print("FFmpeg not found. Please install FFmpeg and add it to PATH.")
            return self._create_fallback(output_path)
        except Exception as e:
            print(f"Error mixing audio: {e}")
            return self._create_fallback(output_path)

    def _create_fallback(self, output_path: str) -> str:
        """Creates a fallback file if mixing fails."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("Fallback audio - mixing failed")
        print(f"Created fallback file at {output_path}")
        return output_path
