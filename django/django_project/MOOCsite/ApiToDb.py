import requests
from xml.etree import ElementTree
from MOOCsite.models import Course, School, Category
import datetime


class ApiToDb:

    def dataSync(self):
        self.CourseraData()
        print ('Coursera')
        self.EdxData()
        self.KhanData()
        self.UdacityData()

    def CourseraData(self):
        #coursera API 1.add fields 2. include linked objects
        #update courses
        i = 0
        #load schools
        schoolUrl = 'https://api.coursera.org/api/partners.v1/'
        schoolRes = requests.get(schoolUrl).json()['elements']
        for school in schoolRes:
            try:
                School.objects.create(pk = school['id'],school_name=school['name'])
            except Exception,e:
                print ("coursera1" + str(e))
        while True :
            courseraUrl = 'https://api.coursera.org/api/courses.v1?fields=description,startDate,partnerIds,primaryLanguages,domainTypes,photoUrl&start='+str(i)
            courseraRes = requests.get(courseraUrl).json()
            for course in courseraRes['elements']:
                try:
                    #load courses
                    courseNew = Course.objects.get_or_create(course_name=course['name'],descriptions=course['description'],provider_id=1,school_id=course['partnerIds'][0],
                                       language=course['primaryLanguages'],photo_url = course['photoUrl'],url='https://www.coursera.org/learn/'+course['slug'])[0]
                    #time
                    try:
                        start_Date = datetime.datetime.fromtimestamp(int(str(course['startDate']/1000))).strftime('%Y-%m-%d')
                        is_Self = False
                    except:
                        start_Date = "1990-01-01"
                        is_Self = True
                    courseType = course['courseType']
                    """if courseType=="v2.ondemand":
                        is_Self = True
                    else:
                        is_Self = False"""
                    duration = "4 to 6 weeks"
                    courseNew.time_set.create(startDate=start_Date,isSelf=is_Self,duration=duration)
                    #load categories
                    cats = course['domainTypes']
                    for cat in cats:
                        try:
                            newCat = Category.objects.get_or_create(category_name = cat['domainId'])[0]
                            courseNew.categories.add(newCat)
                        except Exception,e:
                            print ("coursera2" + str(e))
                except Exception,e:
                    print ("coursera3" +str(e))
            i += 100
            print str(i)+'/'+str(courseraRes['paging']['total'])
            if(i>courseraRes['paging']['total']+100):
                break


    def UdacityData(self):
        print ("Udacity")
        #Udacity API 1.course 2.tracks 3.degrees
        udacityUrl = 'https://www.udacity.com/public-api/v0/courses'
        udacityRes = requests.get(udacityUrl)
        udacityRes = udacityRes.json()
        udacityRes = udacityRes['courses']
        i = 0
        for course in udacityRes:
            try:
                #school
                school = School.objects.get_or_create(school_name=course["affiliates"][0]["name"])[0]
                courseNew = school.course_set.update_or_create(course_name = course['title'] +course['subtitle'],descriptions = course['summary'],
                                                            provider_id=2,url=course['homepage'], photo_url = course['image'])[0]
                #time
                courseNew.time_set.create(startDate="1990-01-01",isSelf=True,duration=str(course['expected_duration'])+' '+course['expected_duration_unit'])
                #categories
                cats = course['tracks']
                for cat in cats:
                    try:
                        newCat = Category.objects.get_or_create(category_name = cat)[0]
                        newCat.save()
                        courseNew.categories.add(newCat)
                    except Exception,e:
                        print ("Udacity" + str(e))
            except Exception,e:
                print ("Udacity2" + str(e))
            print i
            i+=1

    def EdxData(self):
        #Edx API
        edxUrl = 'https://www.edx.org/api/v2/report/course-feed/rss'
        edxRes = requests.get(edxUrl)
        edxRes = ElementTree.fromstring(edxRes.content)
        namespaces = {'course': 'https://www.edx.org/api/course/elements/1.0/'}
        for course in edxRes.iter('item'):
            title = course.find('title').text
            url = course.find('link').text
            description = course.find('description').text
            school = course.find('course:school',namespaces).text
            sdate = course.find('course:start',namespaces).text[0:10]
            try:
                edate = course.find('course:end',namespaces).text[0:10]
            except:
                edate = None
            isSelf = course.find('course:self_paced',namespaces)
            if isSelf.text=='1':
                isSelf=True
            elif isSelf.text=='0':
                isSelf=False
            cats = course.findall('course:subject',namespaces)
            try:
                school = School.objects.get_or_create(school_name=school)[0]
                courseNew = school.course_set.get_or_create(course_name=title,provider_id=3,descriptions=description,url=url, photo_url='https://www.edx.org/sites/default/files/mediakit/image/thumb/edx_logo_200x200.png')[0]
                courseNew.time_set.create(startDate=sdate,endDate=edate,isSelf=isSelf)
                for cat in cats:
                    try:
                        newCat = Category.objects.get_or_create(category_name = cat.text)[0]
                        newCat.save()
                        courseNew.categories.add(newCat)
                    except Exception,e:
                        print ("edx" +str(e))
            except Exception,e:
                print ("edx" +str(e))
        pass



    def KhanData(self):
        #khan api
        #hard code topics
        topics = ["math","science","economics-finance-domain","humanities","computing",
                  "test-prep","partner-content","college-admissions"]
        for topic in topics:
            khanUrl = 'http://www.khanacademy.org/api/v1/topic/'+topic
            khanRes = requests.get(khanUrl)
            khanRes = khanRes.json()
            for course in khanRes["children"]:
                #print course["title"]
                try:
                    courseNew = Course.objects.create(course_name=course['standalone_title']+' '+course["title"],provider_id=4,descriptions=course["description"],
                                                      url=course['url'], photo_url = 'https://cdn.kastatic.org/images/khan-logo-vertical-transparent.png')
                    courseNew.time_set.create(startDate="1990-01-01",isSelf=True,duration="Vary")
                    newCat = Category.objects.get_or_create(category_name = topic)[0]
                    newCat.save()
                    courseNew.categories.add(newCat)
                except Exception,e:
                    print ("khan" +str(e))

sync = ApiToDb()
sync.dataSync()

#python ../manage.py shell
#execfile('ApiToDb.py')