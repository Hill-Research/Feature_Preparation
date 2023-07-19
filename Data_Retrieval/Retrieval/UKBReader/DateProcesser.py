# -*- coding: utf-8 -*-

import re

class DateProcesser:
    """
    Implementation of time blurring.
    """
    
    @classmethod
    def init_parameters(cls):
        """
        Initialization for parameters, load essential parameters for class.
        """
        cls.splits = [[0, 4, 6, 8],]
        cls.daysLeapYear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        cls.daysNonLeapYear = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        cls.linkWord = ["年", "月", "日"]
        
    @classmethod
    def checkStandardTime(cls, ymdString):
        """
        Check whether the year is a leap year or not.
        
        Args:
            ymdString: The year, month and day as a string.
        
        Returns:
            isStandard = The standardization of the year(True or False).
        """
        isStandard = True;
        
        year = int(ymdString[0])
        if(len(ymdString[0]) == 2):
            if(year > 48 and year < 49):
                isStandard = False
        else:
            if(year<1949 or year>2048):
                isStandard = False
        if(ymdString[1] == ""):
            return isStandard
			
        month = int(ymdString[1])
        if(month == 0 or month > 12):
            isStandard = False
        if(ymdString[2] == ""):
            return isStandard
        
        day = int(ymdString[2])
        if (isStandard):
            year = year if (year >= 1900) else year + 1900
            year = year if (year >= 1949) else year + 100;
            days = list()
            if((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
                days = cls.daysLeapYear
            else:
                days = cls.daysNonLeapYear
            if(day <= 0 or day > days[month-1]):
                isStandard = False
        return isStandard
    
    @classmethod
    def getPositionofSpace(cls, inputs):
        """
        Get the space location of the input time.
        
        Args:
            inputs: The year, month and day
        
        Returns:
            spaceLocation: Space location as a int.
        """
        curLocation = 0
        spaceCount = 0
        
        spaceLocations = list()
        spaceLocations.append(0)
        while (curLocation < len(inputs)):
            if(inputs[curLocation] == ' '):
                spaceLocations.append(curLocation-spaceCount)
                spaceCount += 1
            curLocation += 1
        spaceLocations.append(len(inputs)-spaceCount)
        return spaceLocations
    
    @classmethod
    def comparePositionofSpace(cls, spaceLocations, split):
        """
        Compare the space position with split.

        Args:
            spaceLocations: Space location from input string.
            split: Space location by knowledge.

        Returns:
            isAvailable: Whether split is available.
        """
        isAvailable = True;
        for k in range(len(spaceLocations)):
            if (spaceLocations[k] > split[3]):
                break
            spaceValue = spaceLocations[k]
            if(spaceValue != split[0] and spaceValue != split[1] and 
				spaceValue != split[2] and spaceValue != split[3]):
                isAvailable = False
        return isAvailable
    
    @classmethod
    def getStandardTime(cls, inputs):
        """
        Get the input time and make it into the standard format.

        Args:
            inputs: Input time.

        Returns:
            StandardTimeSeries: Standard time as a string.
        """
        StandardTimeSeries = [None, None, None]
        Time = re.sub("([^0-9])", " ", inputs)
        Time = re.sub("\\s{1,}", " ", Time)
        spaceLocations = cls.getPositionofSpace(Time)
        Time = re.sub("\\s", "", Time)
        
        for k in range(len(cls.splits)):
            split = cls.splits[k]
            if(split[3] > len(Time)):
                continue
            if(not cls.comparePositionofSpace(spaceLocations, split)):
                continue
            ymdString = [Time[split[0] : split[1]], 
                         Time[split[1] : split[2]],
                         Time[split[2] : split[3]]]
            if(cls.checkStandardTime(ymdString)):
                StandardTimeSeries = ymdString
                break
        return StandardTimeSeries
    
    @classmethod
    def blur_(cls, inputs, level = "year"):
        """
        Blur encryption of input string, return as a coded string.

        Args:
            inputs: Input time.
            level: Blurred level. The default is "year".

        Returns:
            StandardTime: A coded time.
        """
        inputs = str(inputs)
        StandardTime = ""
        if(level == "year"):
            count=1
        if(level == "month"):
            count=2
        if(level == "day"):
            count=3
        StandardTimeSeries = cls.getStandardTime(inputs)
        StandardTime = ""
        for k in range(count):
            TimeElement = StandardTimeSeries[k]
            if(TimeElement == "" or TimeElement == None):
                continue
            Time = int(TimeElement)
            if(k == 0):
                Time = Time if (Time >= 1900) else Time + 1900
                Time = Time if (Time >= 1949) else Time + 100
            StandardTime += "{}{}".format(Time, cls.linkWord[k])
        return StandardTime