<table>
  <tr>
    <td width="9999px" align="center">
      <p>
        <br>
        <img height="200" src="assets/logo.svg" alt="logo">
      </p>
      <h1>winstall</h1>
      <p>Install your packages and keep them updated.</p>
    </td>
  </tr>
</table>

## Build

```shell
git clone https://github.com/lanzorg/winstall.git
cd ./winstall
pipenv shell
pipenv install
pipenv run build
```

The **winstall.exe** file should be available into the **./winstall/winstall/dist** directory.

## Usage

Make sure you launched cmd or powershell **as administrator** before.

```shell
./winstall.exe -i pkg1 pkg2 pkg3
```

## Packages

| Name                      | Type         | Information                                                              |
|---------------------------|--------------|--------------------------------------------------------------------------|
| android-sdk-cmdline-tools | Development  | The Android SDK command line tools.                                      |
| chromium                  | Internet     | Free and open-source web browser from Google.                            |
| corretto                  | Development  | Multiplatform and production-ready distribution of OpenJDK from Amazon.  |
| figma                     | Graphics     | Collaborative UI design tool built in the browser.                       |
| firefox-developer         | Internet     | Open-source web browser made for developers from Mozilla.                |
| flutter                   | Development  | Google’s UI toolkit for building natively compiled applications.         |
| imposition-wizard         | Office       | PDF imposition software with simple user interface and realtime preview. |
| nodejs                    | Development  | JavaScript runtime built on Chrome's V8 engine.                          |
| picotorrent               | Internet     | Tiny and hackable BitTorrent client.                                     |
| yarn                      | Development  | Fast, reliable, and secure dependency management.                        |
