param (
    [string]$pptx,
    [string]$out,
    [int]$slideNum = 1
)

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx, 1, 0, 0)
$pres.Slides.Item($slideNum).Export($out, 'PNG', 1280, 720)
$pres.Close()
$ppt.Quit()
Write-Host "Exported to $out"
