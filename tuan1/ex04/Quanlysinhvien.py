from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []

    def generateID(self):
        maxid = 1
        if (self.listSinhVien != []):
            maxid = self.listSinhVien[0].id
            for sv in self.listSinhVien:
                if (maxid < sv.id):
                    maxid = sv.id
            maxid = maxid + 1
        return maxid

    def return_self_listSinhVien_len(self):
        return self.listSinhVien.__len__()

    def nhapSinhVien(self):
        sv = self.generateID()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        major = input("Nhap chuyen nganh cua sinh vien: ")
        diemTB = float(input("Nhap diem cua sinh vien: "))
        sv = SinhVien(sv, name, sex, major, diemTB)
        self.listSinhVien.append(sv)

    def updateSinhVien(self, ID):
        sv = None
        for i in range(len(self.listSinhVien)):
            if (self.listSinhVien[i].id == ID):
                sv = self.listSinhVien[i]
                break
        if (sv != None):
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            major = input("Nhap chuyen nganh cua sinh vien: ")
            diemTB = float(input("Nhap diem cua sinh vien: "))
            sv.name = name
            sv.sex = sex
            sv.major = major
            sv.diemTB = diemTB
        else:
            print("Sinh vien co ID = {} khong ton tai.".format(ID))

    def sortByID(self, key=lambda x: x.id, reverse=False):
        self.listSinhVien.sort(key=key, reverse=reverse)

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x.name, reverse=False)

    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x.diemTB, reverse=False)

    def findByID(self, ID):
        searchResult = None
        for sv in self.listSinhVien:
            if (sv.id == ID):
                searchResult = sv
                break
        return searchResult

    def findByName(self, keyword):
        listSV = []
        for sv in self.listSinhVien:
            if (keyword.upper() in sv.name.upper()):
                listSV.append(sv)
        return listSV

    def deleteByID(self, ID):
        isDeleted = False
        for sv in self.findByID(ID):
            if (sv != None):
                self.listSinhVien.remove(sv)
                isDeleted = True
        return isDeleted

    def xepLoaiHocLuc(self, sv:SinhVien):
        if (sv.diemTB >= 9):
            sv.hocLuc = "Xuat sac"
        elif (sv.diemTB >= 8):
            sv.hocLuc = "Gioi"
        elif (sv.diemTB >= 6.5):
            sv.hocLuc = "Kha"
        elif (sv.diemTB >= 5):
            sv.hocLuc = "Trung binh"
        else:
            sv.hocLuc = "Yeu"

    def showSinhVien(self, listSV):
        print("ID".ljust(5), "Name".ljust(15), "Sex".ljust(10), "Major".ljust(15), "Diem TB".ljust(10), "Hoc luc")
        if (listSV != []):
            for sv in listSV:
                print("{:5d} {:15s} {:10s} {:15s} {:10.2f} {:s}".format(sv.id, sv.name, sv.sex, sv.major, sv.diemTB, sv.hocLuc))

    def getListSinhVien(self):
        return self.listSinhVien