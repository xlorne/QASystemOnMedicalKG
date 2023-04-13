<# :
@powershell "icm ([scriptblock]::Create((gc '%~f0' -Raw -Encoding UTF8)))"
exit
#>

jupyter-lab