<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<h1 align="center">Vibe Drive</h1>
  <p align="center">
    <i>An Open Source close replica of Mercedes MBUX Sound Drive</i>
    <br />
    <a href="https://github.com/TFerrarah/Vibe-Drive/issues">Report Bug</a>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
# Getting Started

## Prerequisites

To get Vibe Drive up and running you'll need:
- A computer;
- An OBD-II compatible car (All cars from 1996 onwards should be compatible) / Assetto Corsa / Assetto Corsa Competizione;
- (Only for OBD-II) A working OBD-II adapter (e.g. Bluetooth ELM327 works just fine) and its drivers (when needed)
- A song split in 4 different tracks (You can do so with the <a href="https://github.com/fabiogra/moseca">Moseca</a> free tool)

Also make sure to have these programs installed:
- Python 3
- ffplay
- zmqsend

<details>
  <summary>If you don't have these programs installed...</summary>
  Vibe Drive requires these programs to be installed and working: **Python**, **ffplay**, **zmqsend**

  ### Installing Python
  **Windows**
  ```
  winget install Python.Python3
  ```
  or, alternatively
  ```
  choco install python
  ```
  
  **MacOS**
  ```
  brew install Python
  ```
  
  **Ubuntu/Debian**
  ```
  sudo apt-get install python3
  ```
  
  ### Installing ffmpeg
  
  **Windows**
  ```
  winget install ffmpeg
  ```
  or, alternatively
  ```
  choco install ffmpeg-full
  ```
  
  **MacOS**
  ```
  brew install ffmpeg
  ```
  
  **Ubuntu/Debian**
  ```
  sudo apt-get install ffmpeg
  ```
  
  ### Installing zmqsend
  **Windows**
  <a href="https://www.gyan.dev/ffmpeg/builds/#tools">Download ffmpeg-tools from gyan.dev</a> and add the `bin` folder to your PATH.
  
  **MacOS**
  ```
  brew install zmqsend
  ```
  
  On macOS you can install only zmqsend, which is the only ffmpeg-tool needed
  
  **Ubuntu/Debian**
  ```
  sudo apt-get install libzmq3-dev
  ```
</details>

## Installation

   ```sh
   git clone https://github.com/TFerrarah/Vibe-Drive.git
   cd Vibe-Drive
   pip install -r requirements.txt
   mkdir Audio
   ```

  _An automatic solution is being developed to manage audio files, but for now follow these instructions:_ <br>
  Split your song into 4 files: Bass, Vocals, Drums, Other and place those files in the newly created `Audio` folder. Most audio extensions should work as long as they are supported by your ffmpeg / ffplay installation
  

<!-- USAGE EXAMPLES -->
## Usage

### OBD-II First Run
Plug in your obd adapter with your car turned off
Put your key in MAR position (Only electronics, no engine)
1. Connect your computer to your OBD-II adapter (Bluetooth, Wi-Fi, USB)
2. MAKE SURE TO BE CONNECTED TO THE ADAPTER and run `python main.py` in the Vibe-Drive folder
3. **Follow the on-screen instructions for connection and calibration.**
Keep in mind that the code is written for an ELM327 Bluetooth OBD-II interface, so your might not work properly.

| Adapter Name                           | Baudrate | Protocol |
|----------------------------------------|----------|----------|
| ELM327 Bluetooth                       | 115200   | 7        |
| _Open issue to add your adapter here!_ |          |          |

### OBD-II
Plug in your obd adapter with your car turned off
Put your key in MAR position (Only electronics, no engine)
1. Connect your computer to your OBD-II adapter (Bluetooth, Wi-Fi, USB)
2. MAKE SURE TO BE CONNECTED TO THE ADAPTER and run `python main.py` in the Vibe-Drive folder
3. Follow on-screen instructions for connection
4. Plug in your computer to your car speakers and enjoy!

### Assetto Corsa
1. Open Assetto Corsa / Assetto Corsa Competizione
2. Get to drive a car on track
3. Run `python main.py -s AC`
4. Enjoy.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. **Fork** the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GNU-GPLv3 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Tommaso Ferrara - [@t_ferrarah](https://instagram.com/t_Ferrarah) - tferrarah@gmail.com

Project Link: [https://github.com/TFerrarah/Vibe-Drive](https://github.com/TFerrarah/Vibe-Drive)

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Music Splitting done by Moseca: https://github.com/fabiogra/moseca
* Inspired from: https://github.com/lesageethan/carmony
* Math formulas: https://www.dcode.fr/function-equation-finder
* This YouTube Video: [https://www.youtube.com/watch?v=nIp1GEzF4EY](https://www.youtube.com/watch?v=nIp1GEzF4EY)
* This YouTube Video: [https://www.youtube.com/watch?v=9awdjZlA8BA](https://www.youtube.com/watch?v=9awdjZlA8BA)
* Mercedes and will.i.am for developing MBUX Sound Drive


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TFerrarah/Vibe-Drive.svg?style=for-the-badge
[contributors-url]: https://github.com/TFerrarah/Vibe-Drive/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TFerrarah/Vibe-Drive.svg?style=for-the-badge
[forks-url]: https://github.com/TFerrarah/Vibe-Drive/network/members
[stars-shield]: https://img.shields.io/github/stars/TFerrarah/Vibe-Drive.svg?style=for-the-badge
[stars-url]: https://github.com/TFerrarah/Vibe-Drive/stargazers
[issues-shield]: https://img.shields.io/github/issues/TFerrarah/Vibe-Drive.svg?style=for-the-badge
[issues-url]: https://github.com/TFerrarah/Vibe-Drive/issues
[license-shield]: https://img.shields.io/github/license/TFerrarah/Vibe-Drive.svg?style=for-the-badge
[license-url]: https://github.com/TFerrarah/Vibe-Drive/blob/main/LICENSE
