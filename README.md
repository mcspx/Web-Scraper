# Web-Scraper
Web Scraper Project

1. อ่านรายชื่อพรรคการเมืองจาก https://th.wikipedia.org/wiki/รายชื่อพรรคการเมืองในประเทศไทย มาใช้เป็นข้อมูลตั้งต้น
   ซึ่งข้อมูลจะประกอบไปด้วย -> บันทึกข้อมูลนี้ไว้ใน redis server
	- ชื่อภาษาไทย
	- popular : เก็บจำนวนครั้งที่พบชื่อพรรค
	- counter : เก็บจำนวน url ที่ค้นหา
	- update  : เก็บข้มูลเวลาที่ update ข้อมูลครั้งล่าสุด

2. นำรายชื่อทั้งหมดจาก json ไปค้นหาใน google.co.th แล้วเอา link ทั้งหมดในหน้าแรกของผลการค้นหา มาประมวลผล
	- ค้นหา link ทั้งหมดที่มีใน body แล้วจัดเก็บข้อมูลลง redis server : url link, visit status = 0
		
3. นำข้อมูล link ทั้งหมดที่ได้มาจากขั้นตอนที่ 2 มา call เพื่อ visit แล้วนำ body มาประมวลผลข้อมูล ดังนี้
	- ค้นหาชื่อพรรคการเมืองใน body และทำการนับจำนวน update ค่าข้อมูล popular ของแต่ละพรรคใน redis server
	- update ค่าใน redis server ว่า visit status = 1
	- update ค่าใน 
	- ค้นหา link ทั้งหมดที่มีใน body แล้วจัดเก็บข้อมูลลง redis server : url link, visit status = 0

4. นำข้อมูล link ทั้งหมดที่มีใน redis server มาประมวลแบบในข้อ 3 จนกว่าไม่มีข้อมูลที่ visit status = 0 เหลือให้ประมวลผลแล้ว
   หรือประมวลผลครบ 1,000 รายการแล้ว ค่า counter > 1,000 ให้หยุดทำงาน
