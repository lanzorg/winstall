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

| Name                      | Information                                                       |
|---------------------------|-------------------------------------------------------------------|
| android-sdk-cmdline-tools | The Android SDK command line tools.                               |
| chromium                  | Free and open-source web browser from Google.                     |
| corretto                  | Production-ready distribution of OpenJDK from Amazon.             |
| figma                     | Collaborative UI design tool built in the browser.                |
| firefox-developer         | Open-source web browser made for developers from Mozilla.         |
| flutter                   | Google’s UI toolkit for building natively compiled applications.  |
| imposition-wizard         | Imposition software with simple GUI and realtime preview.         |
| nodejs                    | JavaScript runtime built on Chrome's V8 engine.                   |
| picotorrent               | Tiny and hackable BitTorrent client.                              |
| yarn                      | Fast, reliable, and secure dependency management.                 |
