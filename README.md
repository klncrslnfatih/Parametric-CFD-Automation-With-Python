# Parametric-CFD-Automation-With-Python
A script that automates parametric analysis on Fluent

![automation-example](https://github.com/klncrslnfatih/Parametric-CFD-Automation-With-Python/assets/80931164/7990aae1-55a1-4c0f-abdb-c2a618b1fba3)

With Parametric-CFD-Automation-with-Python, which I used in my undergraduate graduation project, parametric analyses can be performed locally and in HPC much less costly.
This program takes data from Excel and creates journal files and folders in accordance with different parameters. It runs Fluent via the Commander and performs analyses locally. Saves-reports analysis results and creates cl-alpha and cd-alpha graphs via matplotlib. Performs the operations via TUI in a very short time instead of hours with the GUI. Additionally contains alternative TUI scripts for different types of turbulence models. Also it creates a merged file to perform analyses compatible with HPC (High Performance Computing). I would like to thank Rıdvan Taşcıoğlu, my industrial advisor, who helped me create the program.


Merhaba. Ben Fatih KILINÇARSLAN. Bu kod, Lisans bitirme projemi yaparken kullandığım CFD otomatize etme işlemlerini içinde
bulundurmaktadır. TUI kodlarının tamamı ANSYS Fluent 2022 R1'e uygun olacak şekilde yazılmıştır. Kullanımı şu şekildedir:
1. Kullanılacak TUI kodu manipüle edilmeli ve gerekli değişiklikler (sürüme göre) yapılmalıdır. (Örnek TUI kodları "tui-codes"
isimli klasörde bulunmaktadır.)
2. Aynı dizinde analizlerin istenilen parametrelerini bulunduran "cfd-values.xlsx" adında bir excel dosyası olmalıdır.
3. Cmd üzerinden fluent çalıştırılmaya uyumlu olduktan sonra "cfd-parametric.py" üzerine tıklanarak program çalıştırılabilir.
4. Program çalıştırıldıktın sonra klasörler ve journal dosyalarını oluşturmaktadır. Analizlerin lokalde gerçekleştirilmesi
isteniyorsa "enter" e basılarak işlemler devam ettirilebilir.
5. Excel içerisinde belirlenen tüm analizler yapıldıktan sonra sonuçları oluşturacak ve program kendisini kapatacaktır.

Hello. I am Fatih KILINÇARSLAN. This code includes the CFD automation processes that I used while doing my undergraduate graduation
project. All TUI codes were written to be compatible with ANSYS Fluent 2022 R1. Its usage is as follows:
1. The TUI code to be used must be manipulated and the necessary changes must be made (according to the version). (Sample TUI codes
are in the folder named "tui-codes")
2. There must be an excel file named "cfd-values.xlsx" in the same directory that contains the desired parameters of the analysis.
3. After it is compatible with running Fluent via cmd, the program can be run by clicking on "cfd-parametric.py".
4. After the program is run, it creates folders and journal files. If you want to perform the analyzes locally, you can continue the
processes by pressing "enter".
5. After all the analyzes specified in Excel are done, it will create the results and the program will close itself.

Github: @klncrslnfatih
LinkedIn: /fatihkilincarslan
