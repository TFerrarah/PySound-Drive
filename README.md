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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started
Make sure to have these programs installed:
- Python 3
- ffplay
- zmqsend

## Prequisites

<details>
  <summary>Installing Python3, ffmpeg, ffmpeg-tools</summary>
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
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### OBD-II First Run
Plug in your obd adapter with your car turned off
Put your key in MAR position (Only electronics, no engine)
1. Connect your computer to your OBD-II adapter (Bluetooth, Wi-Fi, USB)
2. MAKE SURE TO BE CONNECTED TO THE ADAPTER and run `python main.py` in the Vibe-Drive folder
3. **Follow the on-screen instructions for calibration.**
Keep in mind that the code is written for an ELM327 Bluetooth OBD-II interface, so your might not work properly.

| Adapter Name                           | Baudrate | Protocol |
|----------------------------------------|----------|----------|
| ELM327 Bluetooth                       | 115200   | 7        |
| _Open issue to add your adapter here!_ |          |          |

### Assetto Corsa

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/TFerrarah/Vibe-Drive/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/TFerrarah/Vibe-Drive](https://github.com/TFerrarah/Vibe-Drive)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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
[license-url]: https://github.com/TFerrarah/Vibe-Drive/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
