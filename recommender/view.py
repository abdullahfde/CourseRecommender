# -*- coding: utf-8 -*-

__author__ = 'abdullahfadel'

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from recommendations import *

from django.conf import settings
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import xlrd

from BeautifulSoup import *
from urllib2 import *
from forms import *
from models import *
from django.contrib.auth import authenticate, login, logout

GradingSystem = {'A+': 4.1, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                 'D+': 1.3, 'D': 1.0, 'D-': 0.5, 'F': 0.0, 'S': 0.0}
OutputGrading = {(4.0, 5.0): 'A+', (3.7, 4.0): 'A', (3.3, 3.7): 'A-', (3.0, 3.3): 'B+', (2.7, 3.0): 'B',
                 (2.3, 2.7): 'B-', (2.0, 2.3): 'C+', (1.7, 2.0): 'C',
                 (1.3, 1.7): 'C-', (1.0, 1.3): 'D+', (0.5, 1.0): 'D', (0.1, 0.5): 'D-', (0.0, 0.1): 'F'}

escap_list = ['F(R)', 'D-(R)', 'D(R)', 'D+(R)', 'C-(R)', 'C(R)', 'C+(R)', 'W', 'B-(R)', 'B(R)', 'B+(R)', 'IA(R)',
              'IA', 'U(R)', 'U', 'LA', 'NP', 'CW', 'TP', 'E', 'T', 'I']
Data = {}
DataCatgory = {}


def pdfparser(filename, txtfile):
    t = os.path.join(settings.MEDIA_ROOT, txtfile + '.txt')

    fb = file(filename, 'rb')

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    df = open(t, 'w')
    str = ""
    for page in PDFPage.get_pages(fb):
        interpreter.process_page(page)
        data = retstr.getvalue()
        str = str + data

    df.write(str)
    df.close()
    df = open(t, 'r')
    course_dict = {}
    course_codes = []
    grades = []
    info = []
    semesters = []
    donemstr = ''

    for line in df:
        line.decode("utf-8")

        course_code = re.findall("[A-Z]+\s[0-9]+[A-Z]?", line)

        grade = re.findall("(^[A-Z]{1,2}[-%s]?)\n" % (re.escape('+')), line)

        repeat = re.findall('(^[A-Z]{1,2}[-%s]?%s)\n' % (re.escape('+'), re.escape('(R)')), line)
        withdraw = re.findall('\s[0-9][,.][0-9]+\s(W)\n', line)
        donem = re.findall('[0-9]+%s[0-9]+.*nemi' % re.escape('-'), line)

        donem2 = re.findall('[0-9]+%s[0-9]+.*mester' % re.escape('-'), line)
        if line.startswith(':'):
            inf = line.strip(': ')
            if inf not in info:
                info.append(inf)

        elif course_code:
            course_codes.append(course_code[0])

        elif donem:
            semesters.append(donem)
            if len(course_codes) != 0:
                if len(course_codes) == len(grades):
                    for i in range(len(course_codes)):
                        course_dict[donemstr].setdefault(course_codes[i])
                        course_dict[donemstr][course_codes[i]] = grades[i]
                    course_codes = []
                    grades = []
            donemstr = donem[0]
            course_dict.setdefault(donem[0], {})

        elif donem2:
            semesters.append(donem2)
            if len(course_codes) != 0:
                if len(course_codes) == len(grades):
                    for i in range(len(course_codes)):
                        course_dict[donemstr].setdefault(course_codes[i])
                        course_dict[donemstr][course_codes[i]] = grades[i]
                    course_codes = []
                    grades = []
            donemstr = donem2[0]
            course_dict.setdefault(donem2[0], {})
        elif grade:
            grades.append(grade[0])
        elif withdraw:
            grades.append(withdraw[0])
        elif repeat:

            grades.append(repeat[0])
    if len(course_codes) != 0:
        if len(course_codes) == len(grades):
            for i in range(len(course_codes)):
                course_dict[donemstr].setdefault(course_codes[i])
                course_dict[donemstr][course_codes[i]] = grades[i]
    semesters.sort()

    name, surname, faculty, department, level = info[0].strip('\n'), info[1].strip('\n'), info[7].strip('\n'), info[
        8].strip('\n'), info[9].strip('\n')

    # escap_list = ['F(R)', 'D-(R)', 'D(R)', 'D+(R)', 'C-(R)', 'C(R)', 'C+(R)', 'W', 'B-(R)', 'B(R)', 'B+(R)', 'IA(R)',
    # 'IA', 'U(R)', 'U', 'LA', 'NP', 'CW', 'TP', 'E', 'T', 'I']


    fb.close()
    # Department = unicode(department, 'utf-8').encode('utf-8')

    return course_dict


def get_data(request):
    checkinguser = []
    savelist = []
    student_course = {}
    student_courseSaved = {}
    SaveDate = []
    DateAndUsers = {}

    global recommended_stuff, IdCur, formForChoice, wait, CourseRep, SearchForcur, all_data

    if request.method == 'POST':
        username = 'Current Student'

        form = DocumentForm(request.POST or None, request.FILES or None)

        ChoseDepartForCUR = FormForChoseDepartments(request.POST)
        SettingsForms1 = SettingsForms(request.POST)
        if ChoseDepartForCUR.is_valid():
            IdCur = ChoseDepartForCUR.cleaned_data['select']
            CourseRep = ReplecmentCourse.objects.filter(id=IdCur).values('ReplecmentCourse')
            SearchForcur = Curriculum.objects.filter(id=IdCur).values('Curriculum')

        if form.is_valid():

            paramFile = request.FILES['docfile']

            obj1 = transcripts()
            obj1.files = paramFile
            obj1.save()
            gertrans = transcripts.objects.values('files')
            for bv in gertrans:
                for trans in bv.values():
                    # path = default_storage.save('s1.PDF', ContentFile(paramFile.read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, trans)

                    all_data = pdfparser(tmp_file, 'hello')

            list_course = all_data.values()
            for i in list_course:
                for j, k in i.items():
                    if k in escap_list:
                        continue

                    if SettingsForms1.is_valid():
                        if request.user.is_authenticated():
                            username = request.user.username
                            student_course.setdefault(username, {})
                            student_course[username][j] = GradingSystem[k]

                    if username == 'Current Student':
                        student_course.setdefault('Current Student', {})
                        student_course['Current Student'][j] = GradingSystem[k]

            if SettingsForms1.is_valid():
                if request.user.is_authenticated():
                    for notsaved in SavingTrancript.objects.values('Saving'):
                        for loopin1 in notsaved.values():
                            for usernameSaved, notsaved2 in loopin1.items():
                                checkinguser.append(str(usernameSaved))

                if username not in checkinguser and username != 'Current Student':
                    saving = SavingTrancript()
                    student_courseSaved.setdefault(username, {})

                    student_courseSaved[username]['Department'] = IdCur
                    student_courseSaved[username]['Transcript'] = student_course
                    student_courseSaved[username]['Date'] = (time.strftime("%d/%m/%Y"))

                    saving.Saving = student_courseSaved
                    saving.save()

                else:
                    if username != 'Current Student':

                        for updatedict in SavingTrancript.objects.values('Saving'):

                            for refreshdict in updatedict.values():
                                for keyUserName, valueTranscript in refreshdict.items():
                                    if keyUserName == username:
                                        student_courseSaved.setdefault(username, {})

                                        student_courseSaved[username]['Department'] = IdCur
                                        student_courseSaved[username]['Transcript'] = student_course
                                        student_courseSaved[username]['Date'] = (time.strftime("%d/%m/%Y"))
                        for replacedata in SavingTrancript.objects.values():
                            for keySa, valueSa in replacedata.items():
                                if keySa == 'Saving':
                                    for kk, vv in valueSa.items():
                                        if kk == username:
                                            IdUser = replacedata.get('id')

                                            RefreshData = SavingTrancript.objects.get(id=IdUser)
                                            RefreshData.Saving = student_courseSaved
                                            RefreshData.save()

            Data_all = SomeObject.objects.values('args')
            for data in Data_all:
                for i, j in data.items():
                    for x, y in student_course.items():
                        for k, c in y.items():
                            if k not in j.keys():
                                y.pop(k)

                    recommended_stuff = getRecommendedItems(student_course, j, username)

                transcripts.objects.filter().delete()

            return redirect('/Result/')



    else:

        usernamelists = SavingTrancript.objects.values('Saving')
        for loopin in usernamelists:
            for loopin1 in loopin.values():
                for keyusers, valueloop in loopin1.items():

                    for key1, val1 in valueloop.items():

                        if key1 == 'Date':
                            DateAndUsers[keyusers] = val1

        formForChoice = FormForChoseDepartments()
        form = DocumentForm()
        SettingsForms1 = SettingsForms()
        wait = DateAndUsers

    return render_to_response('Home.html',
                              {'form': form, 'formForChoice': formForChoice, 'SettingsForms1': SettingsForms1, 'wait':
                                  wait},
                              context_instance=RequestContext(request))


def UserSaved(request):
    global CourseRep, SearchForcur, recommended_stuff
    check = SavingTrancript.objects.values('Saving')
    if request.user.is_authenticated():
        username = request.user.username
        for findTrancript in check:
            for userVal in findTrancript.values():

                for Keyuser, valueuser in userVal.items():
                    if Keyuser == username:
                        for keyuserssaved, valueUsersSaved in valueuser.items():
                            if keyuserssaved == 'Department':

                                CourseRep = ReplecmentCourse.objects.filter(id=valueUsersSaved).values(
                                    'ReplecmentCourse')
                                SearchForcur = Curriculum.objects.filter(id=valueUsersSaved).values('Curriculum')
                            elif keyuserssaved == 'Transcript':
                                Data_all = SomeObject.objects.values('args')
                                for getdata in Data_all:
                                    for i, fd in getdata.items():
                                        for x, y in valueUsersSaved.items():
                                            for k, c in y.items():
                                                if k not in fd.keys():
                                                    y.pop(k)

                                        recommended_stuff = getRecommendedItems(valueUsersSaved, fd, username)
    keysList = []
    PassToDatas = []

    for KEY, VAL in recommended_stuff:
        for i in CourseRep:
            for key, value in i.items():
                checking = bool(value)
                if checking == True:
                    for key1, value1 in value.items():

                        if key1 == VAL:
                            keysList.append(key1)
                            NewRecommended_stuff = update_in_alist(recommended_stuff, KEY, value1)
                            PassToData = MapDATA(NewRecommended_stuff)
                            for appendData1 in PassToData:
                                # if key1 in PassToData:
                                # PassToData.remove(key1)
                                if appendData1 not in PassToDatas:
                                    PassToDatas.append(appendData1)

                        else:
                            NoMatch = MapDATA(recommended_stuff)
                            for appendData2 in NoMatch:
                                if appendData2 not in PassToDatas:
                                    PassToDatas.append(appendData2)



                else:
                    NoMatch1 = MapDATA(recommended_stuff)
                    for appendData3 in NoMatch1:
                        if appendData3 not in PassToDatas:
                            PassToDatas.append(appendData3)

    for search in keysList:
        for keys, vals in PassToDatas:
            if keys == search:
                PassToDatas.remove((keys, vals))

    man = []
    departmentalElective = []
    uni = []
    general = []
    FinalData = {}
    newGeneral = []
    newMan = []
    newDepartmentElective = []
    newUni = []

    offeringCourses = OfferedCourses.objects.filter(id=1).values('AllCourses')

    for i in SearchForcur:
        for k, dic1 in i.items():
            for c, v in PassToDatas:

                if c in dic1['Mandatory Courses']:
                    if (c, v) not in man:
                        man.append((c, v))
                elif c in dic1['Departmental Elective']:
                    if (c, v) not in man:
                        departmentalElective.append((c, v))


                elif c in dic1['UNI Courses']:
                    if (c, v) not in uni:
                        uni.append((c, v))
                else:
                    if (c, v) not in general:
                        general.append((c, v))

    for all in offeringCourses:
        for key, value in all.items():
            for IndexValue in value:
                for K, V in general:
                    if IndexValue == K:
                        if (K, V) not in newGeneral:
                            newGeneral.append((K, V))
                for K1, V1 in man:
                    if IndexValue == K1:
                        newMan.append((K1, V1))
                for K2, V2 in departmentalElective:
                    if IndexValue == K2:
                        newDepartmentElective.append((K2, V2))
                for K3, V3 in uni:
                    if IndexValue == K3:
                        newUni.append((K3, V3))

    FinalData['Mandatory Courses'] = newMan
    FinalData['Departmental Elective'] = newDepartmentElective
    FinalData['UNI Course'] = newUni

    FinalData['General Course'] = newGeneral

    return render_to_response('Results.html',
                              {'FinalData': FinalData, 'newMan': newMan, 'newDepartmentElective': newDepartmentElective,
                               'newUni': newUni, 'newGeneral': newGeneral}, RequestContext(request))


def Offered_Courses(URL):
    request = Request(URL)
    response = urlopen(request)
    html_version = response.read()
    soup = BeautifulSoup(html_version)
    s = []
    OfferedCourse = []
    All_informations = [i.text for i in soup.fetch('span') if (('style' in dict(i.attrs)))]

    for i in All_informations:
        course_code1 = re.findall("[A-Z]+\s[0-9]+[A-Z]?", i)
        s.append(course_code1)
        course_code2 = re.findall("[A-Z]+\s[0-9]+[A-Z]{2,}", i)
        course_code3 = re.findall("[A-Z]+\s[0-9]+\s[L]?", i)
        s.append(course_code2)
        s.append(course_code3)
    for i in s:
        for b in i:
            if b not in OfferedCourse:
                OfferedCourse.append(b)
    return OfferedCourse


def update_in_alist(alist, key, value):
    return [(k, v) if (k != key) else (key, value) for (k, v) in alist]


def update_in_alist_inplace(alist, key, value):
    alist[:] = update_in_alist(alist, key, value)


def MapDATA(recommended_stuffs):
    formated = []

    for item in recommended_stuffs:
        for range in OutputGrading.keys():
            # if range[0] < item[0] and item[0] < range[1]:
            if item[0] > range[0] and item[0] <= range[1]:
                formated.append((item[1], str('%.2f ' % item[0]) + OutputGrading[range]))
    return formated


def get_recommendations(request):
    keysList = []
    PassToDatas = []

    for KEY, VAL in recommended_stuff:
        for i in CourseRep:
            for key, value in i.items():
                checking = bool(value)
                if checking == True:
                    for key1, value1 in value.items():

                        if key1 == VAL:
                            keysList.append(key1)
                            NewRecommended_stuff = update_in_alist(recommended_stuff, KEY, value1)
                            PassToData = MapDATA(NewRecommended_stuff)
                            for appendData1 in PassToData:
                                # if key1 in PassToData:
                                # PassToData.remove(key1)
                                if appendData1 not in PassToDatas:
                                    PassToDatas.append(appendData1)

                        else:
                            NoMatch = MapDATA(recommended_stuff)
                            for appendData2 in NoMatch:
                                if appendData2 not in PassToDatas:
                                    PassToDatas.append(appendData2)



                else:
                    NoMatch1 = MapDATA(recommended_stuff)
                    for appendData3 in NoMatch1:
                        if appendData3 not in PassToDatas:
                            PassToDatas.append(appendData3)

    for search in keysList:
        for keys, vals in PassToDatas:
            if keys == search:
                PassToDatas.remove((keys, vals))

    man = []
    departmentalElective = []
    uni = []
    general = []
    FinalData = {}
    newGeneral = []
    newMan = []
    newDepartmentElective = []
    newUni = []

    offeringCourses = OfferedCourses.objects.filter(id=1).values('AllCourses')

    for i in SearchForcur:
        for k, dic1 in i.items():
            for c, v in PassToDatas:

                if c in dic1['Mandatory Courses']:
                    if (c, v) not in man:
                        man.append((c, v))
                elif c in dic1['Departmental Elective']:
                    if (c, v) not in man:
                        departmentalElective.append((c, v))


                elif c in dic1['UNI Courses']:
                    if (c, v) not in uni:
                        uni.append((c, v))
                else:
                    if (c, v) not in general:
                        general.append((c, v))

    for all in offeringCourses:
        for key, value in all.items():
            for IndexValue in value:
                for K, V in general:
                    if IndexValue == K:
                        if (K, V) not in newGeneral:
                            newGeneral.append((K, V))
                for K1, V1 in man:
                    if IndexValue == K1:
                        newMan.append((K1, V1))
                for K2, V2 in departmentalElective:
                    if IndexValue == K2:
                        newDepartmentElective.append((K2, V2))
                for K3, V3 in uni:
                    if IndexValue == K3:
                        newUni.append((K3, V3))

    FinalData['Mandatory Courses'] = newMan
    FinalData['Departmental Elective'] = newDepartmentElective
    FinalData['UNI Course'] = newUni

    FinalData['General Course'] = newGeneral

    return render_to_response('Results.html',
                              {'FinalData': FinalData, 'newMan': newMan, 'newDepartmentElective': newDepartmentElective,
                               'newUni': newUni, 'newGeneral': newGeneral}, RequestContext(request))


def login_user(request):
    logout(request)

    if request.method == 'POST':

        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/admin_tools/')

    return render_to_response('admin-login.html', context_instance=RequestContext(request))


def admin_tools(request):
    return render_to_response('admin-tools.html', context_instance=RequestContext(request))


def SaveCurriculum(FileName):
    Z = []
    ignor = []
    MandatoryCourses = []
    Z1 = []
    Courses = []
    UniCourses = []
    DataCatgory = {}

    semster = ["Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI", "Semester VII",
               "Semester VIII"]
    excel_file = xlrd.open_workbook(filename=None, file_contents=FileName.read())

    info = excel_file.sheet_by_index(0)
    for k in semster:
        for row in range(1, info.nrows):
            for i in range(info.ncols):
                if info.cell(row, i).value == k:

                    while len(info.cell(row, i).value) != 0:  # while value of the cell is not 0
                        Z.append(str(info.cell(row + 2, i).value))
                        row += 1

    for m in Z:
        course = re.match("UNI+\s[0-9]+[A-Z]?", m)
        if course:
            ignor.append(course.group())

        course = re.match("UNI+\s[x][x][x]?", m)
        if course:
            ignor.append(course.group())

        course = re.match("[x][x][x]?", m)
        if course:
            ignor.append(course.group())
        course = re.match("[A-Z]+\s[x][x][x]?", m)
        if course:
            ignor.append(course.group())

    for c in Z:
        if c not in MandatoryCourses:
            MandatoryCourses.append(c)
            if c == "":
                MandatoryCourses.remove(c)

    for l in ignor:
        if l in MandatoryCourses:
            MandatoryCourses.remove(l)

    info = excel_file.sheet_by_index(0)
    for i in range(info.ncols):
        for row in range(1, info.nrows):
            CourseCode1 = str(info.row(row)[i]).split("\'")
            Z1.append(CourseCode1)
        for i in Z1:
            for j in i:

                course_code2 = re.findall("[A-Z]+\s[0-9]+[A-Z]?", j)
                for i in course_code2:

                    course_code3 = re.findall(r"[A-Z]{2,}\s[0-9a-zA-Z]{3,}$", i)
                    for k in course_code3:
                        if k not in Courses:
                            Courses.append(k)

    for i in Courses:

        course = re.match("UNI+\s[0-9]+[A-Z]?", i)
        if course:
            UniCourses.append(course.group())
    for i in UniCourses:
        if i in Courses:
            Courses.remove(i)
    for ForData in MandatoryCourses:
        if ForData in Courses:
            Courses.remove(ForData)

    DataCatgory['Departmental Elective'] = Courses
    DataCatgory['UNI Courses'] = UniCourses
    DataCatgory['Mandatory Courses'] = MandatoryCourses
    return DataCatgory


def AddDepartmentElectives(course, IDdepartmental):
    FindDepartment = Curriculum.objects.filter(id=IDdepartmental).values('Curriculum')
    for i in FindDepartment:
        for j in i.values():
            for key, value in j.items():
                if key == 'Departmental Elective':
                    value.append(course)
            return j


def RemoveDepartmentalElectivesCourse(course, IDdepartmental):
    FindDepartment = Curriculum.objects.filter(id=IDdepartmental).values('Curriculum')
    for i in FindDepartment:
        for j in i.values():
            for key, value in j.items():
                if key == 'Departmental Elective':
                    if course in value:
                        value.remove(course)
            return j


def ReplecmentCoursesFun(oldCourse, newCourse, IDdep):
    global dict1
    CourseRep = ReplecmentCourse.objects.filter(id=IDdep).values('ReplecmentCourse')
    for dictOF in CourseRep:
        for key, dict1 in dictOF.items():
            dict1[oldCourse] = newCourse
        return dict1


def EditDepartmentalElectiveCourse(NewCourse, OldCourse, IDdepartmental):
    FindDepartment = Curriculum.objects.filter(id=IDdepartmental).values('Curriculum')

    for i in FindDepartment:
        for j in i.values():
            for key, value in j.items():
                if key == 'Departmental Elective':
                    if OldCourse in value:
                        value.remove(OldCourse)
                        value.append(NewCourse)
            return j


def my_view(request):
    global DataCur, my_choice_field, n
    if request.method == 'POST':

        form1 = MyForm(request.POST)
        form2 = exlForm(request.POST or None, request.FILES or None)

        if form1.is_valid():
            my_choice_field = form1.cleaned_data["MyForms"]
        if form2.is_valid():
            exldoc = request.FILES['docfile']
            DataCur = SaveCurriculum(exldoc)

            obj = Curriculum.objects.get(id=my_choice_field)
            obj.Curriculum = DataCur
            obj.save()
            return HttpResponseRedirect('/test/')

    if request.method == 'POST':
        form3 = AddForm(request.POST)
        form4 = addexlForm(request.POST or None, request.FILES or None)
        if form3.is_valid():
            NameOfCur = form3.cleaned_data["Add"]

            adding = FormForChoseDepartment.objects.values('MyChoice')
            for i in adding:
                for m, n in i.items():
                    n.append((len(n) + 1, NameOfCur))
            seen = set()
            v = [item for item in n if item[1] not in seen and not seen.add(item[1])]

            FormForChoseDepartment.objects.filter().delete()  # here I'm updating the database when I admin wants to add new curriculum
            obj1 = FormForChoseDepartment()
            obj1.MyChoice = v
            obj1.save()
            obj3 = ReplecmentCourse()
            obj3.ReplecmentCourse = {}
            obj3.save()
        if form4.is_valid():
            Addex = request.FILES['docfiles']
            InserData = SaveCurriculum(Addex)
            obj2 = Curriculum()
            obj2.Curriculum = InserData
            obj2.save()
            return redirect('admin-tools')

    if request.method == 'POST':
        form5 = offered_courses(request.POST)
        if form5.is_valid():
            InputUrl = form5.cleaned_data["offered_courses"]
            getting_data_from_function = Offered_Courses(InputUrl)
            RefreshData = OfferedCourses.objects.get(id=1)
            RefreshData.AllCourses = getting_data_from_function
            RefreshData.save()
            return redirect('admin-tools')

    if request.method == 'POST':
        form6 = AddDepartmentalElective(request.POST)
        form7 = SelectDepartmentForAddingCourse(request.POST)
        if form6.is_valid():
            CourseNameForAddingDepElective = form6.cleaned_data['AddCourse']

            if form7.is_valid():
                IDDep = form7.cleaned_data['select']
                PassToAddCourse = AddDepartmentElectives(CourseNameForAddingDepElective, IDDep)
                SaveChanges = Curriculum.objects.get(id=IDDep)
                SaveChanges.Curriculum = PassToAddCourse
                SaveChanges.save()
            return redirect('admin-tools')
    if request.method == 'POST':
        form8 = RemoveDepartmentalEelective(request.POST)
        form9 = SelectDepartmentForRemoveCourse(request.POST)
        if form8.is_valid():
            CourseNameForRemovingDepElective = form8.cleaned_data['RemoveDepElective']
            if form9.is_valid():
                IDDep1 = form9.cleaned_data['select']
                PassToRemoveCourse = RemoveDepartmentalElectivesCourse(CourseNameForRemovingDepElective, IDDep1)
                SaveChanges1 = Curriculum.objects.get(id=IDDep1)
                SaveChanges1.Curriculum = PassToRemoveCourse
                SaveChanges1.save()
            return redirect('admin-tools')
    if request.method == 'POST':
        form10 = OldCourse(request.POST)
        form11 = NewCourse(request.POST)
        form12 = SelectDepartmentForEditCourse(request.POST)
        if form10.is_valid():
            CodeOfOldCourse = form10.cleaned_data['EditOldCourse']
            if form11.is_valid():
                CodeOfNewCourse = form11.cleaned_data['NewCourseEdited']
                if form12.is_valid():
                    DepID = form12.cleaned_data['select']
                    PassToEditCourse = EditDepartmentalElectiveCourse(CodeOfNewCourse, CodeOfOldCourse, DepID)
                    SaveChanges2 = Curriculum.objects.get(id=DepID)
                    SaveChanges2.Curriculum = PassToEditCourse
                    SaveChanges2.save()
            return redirect('admin-tools')
    if request.method == 'POST':
        form13 = Replecmentfrom(request.POST)
        form14 = ReplecmentTo(request.POST)
        form15 = selectDepartmentForReplecmentCourse(request.POST)
        if form13.is_valid():
            OldCode = form13.cleaned_data['Replecmentfromold']
            if form14.is_valid():
                NewCode = form14.cleaned_data['ReplecmentfromNew']
                if form15.is_valid():
                    IDE2 = form15.cleaned_data['select']
                    PassToReplce = ReplecmentCoursesFun(OldCode, NewCode, IDE2)

                    SaveChanges3 = ReplecmentCourse.objects.get(id=IDE2)
                    SaveChanges3.ReplecmentCourse = PassToReplce
                    SaveChanges3.save()
            return redirect('admin-tools')



    else:

        form1 = MyForm()
        form2 = exlForm()
        form3 = AddForm()
        form4 = addexlForm()
        form5 = offered_courses()
        form6 = AddDepartmentalElective()
        form7 = SelectDepartmentForAddingCourse()
        form8 = RemoveDepartmentalEelective()
        form9 = SelectDepartmentForRemoveCourse()
        form10 = OldCourse()
        form11 = NewCourse()
        form12 = SelectDepartmentForEditCourse()
        form13 = Replecmentfrom()
        form14 = ReplecmentTo()
        form15 = selectDepartmentForReplecmentCourse()

    return render_to_response('admin-tools.html',
                              {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5,
                               'form6': form6, 'form7': form7, 'form8': form8, 'form9': form9, 'form10': form10,
                               'form11': form11,
                               'form12': form12, 'form13': form13, 'form14': form14, 'form15': form15},
                              context_instance=RequestContext(request))
