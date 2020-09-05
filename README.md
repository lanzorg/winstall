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
cd winstall
pipenv shell
pipenv install
pipenv run build
```

The **winstall.exe** file should be available into the **./winstall/winstall/dist** directory.

## Usage

```shell
winstall -i pkg1 pkg2 pkg3
```
