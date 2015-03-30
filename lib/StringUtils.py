######################################################
# StringUtils Robot library
# Functions for operations on strings, lines and lists
# Marcin Michalak, NSN Wroclaw, 2008
######################################################
import os
import re
import shutil
import time
import fnmatch
import glob

from robot import utils
from robot.errors import DataError
from types import ListType
from types import StringType
import robot.output
import BuiltIn
builtin = BuiltIn.BuiltIn()


class StringUtils:
    
    """This library contains useful functions related to string operations."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
                        
    def get_first_line(self, lines):
        """
        
      Returns the first line of input: head -1
        """
        multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(multiLines)
        lineCount = len(multiLines)
        if (lineCount == 0): return ""
        return multiLines[0]
    
    def get_head_lines_as_list(self, lines, lineCount):
        """
        
      Returns the first lineCount lines of input: head -lineCount
      as a list
        """
        lineCount = int(lineCount)
        multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(multiLines)
        totalLineCount = len(multiLines)
        if (totalLineCount == 0): return ""
        return multiLines[0 : (lineCount)]

    def get_line_count(self, lines):
        """
        
      Returns the line count
        """
        multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(multiLines)
        lineCount = len(multiLines)
        return lineCount
        
    def get_last_line(self, lines):
        """
        
      Returns the last line of input: tail -1
        """
        multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(multiLines)
        lineCount = len(multiLines)
        if (lineCount == 0): return ""
        return multiLines[lineCount - 1]

    def get_all_but_last_line_as_list(self, lines):
        """
        
      Returns list of all but the last line of input
        """
        multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(multiLines)
        lineCount = len(multiLines)
        if (lineCount == 0): return []
        return multiLines[0 : lineCount - 1]

    def get_all_but_last_line(self, lines):
        """
        
      Returns all but the last line of input as string (cuts out the last line)
        """
        multiLines = lines.splitlines(0)
        allButLast = "";
        print "*INFO* Got '%d' lines" % len(multiLines)
        lineCount = len(multiLines)
        if (lineCount < 2): return ""
        for i in range (0, lineCount - 1):
            allButLast += multiLines[i] + "\n"
        return allButLast

    def get_lines_as_list(self, lines, removeEmptyLines = 0):
        """
        
      Converts multiline input to list of lines. Ends of lines removed.
      If removeEmptyLines != 0, empty lines are removed
      
        """
        LIST__multiLines = lines.splitlines(0)
        print "*INFO* Got '%d' lines" % len(LIST__multiLines)
        lineCount = len(LIST__multiLines)
        if (lineCount == 0): return list()
        if (removeEmptyLines):
            LIST__multiLines = self.remove_empty_elements_from_list(LIST__multiLines)
        return LIST__multiLines

    def remove_empty_elements_from_list(self, elements):
        """
        Removes empty elements from list. Returns list.
        """
        newelements = []
        for i in range (0, len(elements) ):
            print elements[i]
            if (elements[i] != ''):
                newelements.append(elements[i])
        return newelements

    def split_to_last_line_and_rest(self, lines):
        """
        Splits multiline input to all_but_last and last line.
        Returns a list [lastline, all_but_last_line]
        Used for getting RC and output from the command, RC being the last line.
        """
        multiLines = lines.splitlines(0)
        lineCount = len(multiLines)
        if (lineCount < 2):
            retLines = []
            retLines.append(multiLines[0])
            retLines.append('')
            return retLines
        lastLine = multiLines[lineCount - 1]
        # if line before last is empty, remove it - comes from additional \n in the echo
        if (multiLines [lineCount-2] == ""): lineCount = lineCount - 1
        allButLast = ""
        for i in range (0, lineCount - 1):
            allButLast += multiLines[i] + "\n"
        #print retLines
        retLines = [lastLine, allButLast]
        return retLines
    
    def convert_list_to_csv(self, convertList):
        """
        Converts a list of elements to comma-separated element string
        ['a','b','c'] => 'a,b,c'
        """
        result = ''
        if isinstance(convertList, StringType):
            tempList = []
            tempList.append(convertList)
            convertList = tempList
        for listElement in convertList:
            result += listElement + ","
        result = result.rstrip(',')
        return result

    def convert_csv_to_list(self, convertCsv):
        """
        Converts a comma-separated element string to a list of elements
        'a,b,c' => ['a','b','c']
        """
        result = convertCsv.split(',')
        return result

    def get_elements_outside_of_scope_as_lines(self,elements, scopeElements):
        """
        This keyword returns elements without lines where any of linesToExclude is a substring
        Used for finding elements outside of scope
        """
        resultLines = ""
        elementOutsideScope = 1
        for elementToMatch in elements:
            elementOutsideScope = 1
            for scopeElement in scopeElements:
                # check if is a substring
                if (elementToMatch.count(scopeElement)):
                    #print "*TRACE* '%s' does not contain '%s'" % (elementToMatch, scopeElement)
                    elementOutsideScope = 0

            if (elementOutsideScope): resultLines += elementToMatch + "\n"
        return resultLines
        
    def get_lines_not_matching_any_of_elements(self, linesToMatch, linesToExcludeList):
        """
        This keyword returns linesToMatch without lines where any of linesToExclude is a substring
        """
        resultLines = ""
        #raise AssertionError("implementation to be corrected")
        someElementMatches = 0
        linesToMatchList = linesToMatch.splitlines(0)
        for lineToMatch in linesToMatchList:
            someElementMatches = 0
            for lineToExclude in linesToExcludeList:
                # check if is a substring
                if (lineToMatch.count(lineToExclude)):
                    someElementMatches = 1
            if not (someElementMatches): resultLines = lineToMatch + "\n"
        return resultLines
