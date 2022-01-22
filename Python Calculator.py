# example: accuray: 10                                          # rounded to 10 digits
#          values in system: 10                                 # decimal (0-9)
#          expression:  (3^3/18 + 3.8/2 --1.24/(3!^2)) * .01
#          # return: .0343444444


# calculator can reduce an expression typed by the user to
    # an exact value and decimal approximation
    
# current operators are: addition, subtraction, division, multiplication,
    # and integer powers
        
# the user can type expressions in different decimal systems
       # (2 is binary, 10 is decimal, 16 is hexadecimal, ..., up to 62)


# A change I recently made is causing errors with calculating exact value
    # non-integer powers, so I disabled their use. 
import pdb
import math


# add comparison operators (==,>,<,...)

def main():
    global ACCURACY
    global digit_list
    ACCURACY = int(input("Accuracy? "))
    digit_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F",\
        "G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    for digit in digit_list[10:]: # add lowercase values (excluding numbers)
        digit_list.append(digit.lower())
    quantity_of_digits = 0
    custom_list = 0
    valid_list = 0
    # create a separate 'get user value' function
    while not valid_list:
        quantity_of_digits = input("How many values are in the decimal system? ")
        # allow the user to create a 'custom' digit_list
        if quantity_of_digits == "custom":
            custom_list = input("Type a list(ascending order of value): ")
            digit_list = custom_list
            valid_list = True
        else:
            quantity_of_digits = int(quantity_of_digits)
            if not (quantity_of_digits<=len(digit_list) and quantity_of_digits>=2):
                print("Choose a value between "+str(2)+" and "+str(len(digit_list))+".")
            else:
                valid_list = True
                digit_list = digit_list[:quantity_of_digits]
    user_string = input("Type an expression: ")
    if(user_string[0] == "-"):
        user_string = "0" + user_string
    expression = split_into_values(user_string)
    result = final_calc(expression)
    #print("result=",result)
    ###########
    if type(result) == dict:
        print("\nExact Value: ",end="")
        reduce_to_string(result)
    else:
    ############
        print("\nExact Value: "+result[0]+" / "+result[1])
        long_div_result = remove_trailing_zeros(long_division(result,False))
        print("Rounded to "+str(ACCURACY)+" digits: "+\
              (long_div_result))
        print("Exponent: "+decimal_to_exponent(long_div_result))
    

# 3^.25-3^.2
def reduce_to_string(root_val):
    # for every root and subexpression in the root value:
    root_val_index = 0
    for root,subexp in root_val.items():
        # if there is exactly one(non-multiplier) root of value "1":
        if root == digit_list[1]:
            # only print the corresponding subexp in fractional form
            print(str(subexp[0][0][0])+"/"+str(subexp[0][0][1]),end="")
        # otherwise:
        else:
            # do other stuff
            if type(root) != tuple:
                root = (root,)
            exp_index = 0
            # for every expression in the subexpression:
            for expression in subexp:
#                print("(",end="") # adds parentacees for each mult_exp
                # reduce that expression
                # print the expression to the power of 1/root
                fraction_list_index = 0
                for fraction_list in expression:
                    ####################################
                    # if fraction_list is not a list
                    if type(fraction_list)==dict:
                        # initialize declaraction of root_value
                        print("(",end="")
                        # recall the function
                        reduce_to_string(fraction_list)
                        # end with parentacees to the power of (1 / the root value)
                        print(")^("+digit_list[1]+"/"+root[fraction_list_index]+")",end="")
                    else:
                        # do other stuff
                    ####################################
                        # if the value is the 'multiplier'
                        if fraction_list_index == 0:
                            # only print if the multiplier is not "1"
                            if fraction_list[0]!=digit_list[1] or fraction_list[1]!=digit_list[1]:
                                # if the denominator is 1:
                                if fraction_list[1] == digit_list[1]:
                                    # only print the numerator
                                    print(fraction_list[0]+"*",end="")
                                else:
                                    # print both
                                    print("("+fraction_list[0]+"/"+fraction_list[1]+")*",end="")
                        else:
                            # if the index is not first:
                            if fraction_list_index>1:
                                # do not print "*" before the second value(before multiplier)
                                print("*",end="")
                            # print the base
                            # if the denominator is 1 or -1
                            if fraction_list[1] == digit_list[1]:
                                # only print the numerator
                                print(fraction_list[0],end="")
                            else:
                                print("("+fraction_list[0]+"/"+fraction_list[1]+")",end="")
                            # if the root is not 1:
                            if root[fraction_list_index-1]!=digit_list[1]:
                                # print the power
                                print("^("+digit_list[1]+"/"+root[fraction_list_index-1]+")",end="")
                            # else:
                                # do not print anything
                    fraction_list_index += 1
                exp_index += 1
#                print(")",end="") # adds paentacees for each mult_exp
                # add "+" between inner root expressions (exlude after last term)
                if exp_index<len(subexp):
                    print(" + ",end="")
        root_val_index += 1  
        if root_val_index<len(root_val.keys()):
            print(" + ",end="")

# EXAMPLE: remove_power_1({('2', '3'): [[['1', '1'], ['3', '1'], ['7', '1']]], ('5', '2', '1'): [[['4', '1'], ['27', '1'], ['6', '1'], ['1', '1']]]})
# if there are two elements any expression(multiplier and base):
    # and the(one) root value is equal to "1":
        # change the dictionary into a list containing the multiplier
def remove_power_1(root_expression):
    # for every expression within the root_expression:
    for root_tuple,root_exp in root_expression.items():
        init_root_tuple = root_tuple
        # while "1" is in the tuple of roots:
        while digit_list[1] in root_tuple:
            # find the index of the "1" WRT the tuple
            index = root_tuple.index(digit_list[1])
            # for every sub_expression in the root_exp:
            sub_exp_index = 0
            for sub_exp in root_exp:
                multiplier = root_expression[root_tuple][sub_exp_index][0]
                base_of_1 = root_expression[root_tuple][sub_exp_index][index+1]
                # find the root_base corresponding to the index of the "1"
                # multiply the multiplier by that root_base
                root_expression[root_tuple][sub_exp_index][0]=operator_mult_two([multiplier,base_of_1])
                # remove the root_base
                root_expression[root_tuple][sub_exp_index].pop(index+1)
                sub_exp_index += 1
            # remove the "1" from the tuple
            root_tuple = root_tuple[:index]+root_tuple[index+1:]

            # add the new value
            root_expression[init_root_tuple]=root_expression[init_root_tuple]
            # remove the old value
            root_expression.pop(init_root_tuple)
    return root_expression
    
def decimal_to_exponent(value):
    shifted = digit_list[0] # when decimal shifted right, add 1
    if value[0] == "-": # remove negative and add it at end
        value = value[1:]
        negative = True
    else:
        negative = False
    if "." not in value:
        value += "."
    dec_index = value.index(".")
    while value[0] == ".":
        # more the decimal point 1 right
        value = value[1] + "." + value[2:]
        # if the first digit is zero, remove it
        if value[0] == digit_list[0]:
            value = value[1:]
        shifted = det_addsub(shifted,"-"+digit_list[1])
    # find the decimal index
    dec_index = value.index(".")
    # find the value without a decimal
    value = value[:dec_index] + value[dec_index+1:]
    if len(value) == 1:
        decimal = False
    else:
        decimal = True
    # put the decimal at the second element
    value = value[0] + "."*decimal + value[1:]
    inner_value = det_addsub(decimal_to_digit_system(dec_index),"-"+digit_list[1])
    shifted = det_addsub(shifted,inner_value)
    # remove trailing zeros from shifted
    value = value + (" E" + shifted)
    return negative*"-" + value

def split_into_values(string_par):
    string = ""
    for character in string_par:
        if character in "/*-+!().^" or character in digit_list: # operator
            # if the last character is an operator that cannot be followed by another operator
            if character in "^/*+!": # may need to add "(" or ")"
                if string[-1] in "^/*+(": # may need to check "(" and ")" (and "-")
                    # state that the operator is invalid
                    print("'"+character + "' cannot follow another operator.")
                    raise ValueError
            string += character
        else:
            if character != " ":
                print("'",character,"' is not a valid character, and will be ignored.",sep="")
    expression_list = [""]
    index = 0
    for character in string:
        if character in "^+-/*!()":
            if expression_list[index] == "-":
                expression_list[index] += digit_list[1]
                expression_list.append("*")
                index += 1
            expression_list.append(character)
            expression_list.append("")
            index += 2
        else:
            expression_list[index] += character
    for index in range(len(expression_list)):
        if not expression_list[index] in "^+-/*()!.":
            expression_list[index]=remove_decimal(split_by_slash(expression_list[index]))
    # remove empty elements
    while '' in expression_list:
        expression_list.remove('')
    # for every index in the list(excluding the first)
    for index in range(1,len(expression_list)):
        if type(expression_list[index-1]) == str:
            # if the value is "-" and the previous value cannot be subtraced from
            if expression_list[index] == "-" and expression_list[index-1] in "(+/^*-":
                # move the "-" to the next element's numerator
                expression_list[index] = ""
                expression_list[index+1][0] = "-"+expression_list[index+1][0]
    while '' in expression_list:
        expression_list.remove('')
    return expression_list

def final_calc(expression):
    while "(" in expression:
        # evaluate the smallest expression
        expression = eval_smallest_expression(expression)
    result = eval_wo_par(expression)
    return result

def eval_smallest_expression(expression):
    result = find_no_par(expression)
    expression = result[0]
    start_bound = result[1]
    end_bound = result[2]
    simple_express = expression[start_bound:end_bound+1]
    # transform the first parantace into the result
    expression[start_bound-1]=eval_wo_par(simple_express)
    # remove from the first element to the end parantacees
    for removal in range(start_bound-1,end_bound+1):
        expression.pop(start_bound)
    return expression

def find_no_par(expression):
    orig_expression = expression
    first_index = 0
    while "(" in expression or ")" in expression:
        if not ("(" in expression and ")" in expression):
            if "(" in expression:
                print("There is an unmatched \"(\".")
            else:
                print("There is an unmatched \")\".")
            return int("3.5")
        else:
            result = find_parantacees(expression)
            expression = result[0]
            first_index += result[1]+1 # shows index of first element IN inner expression
            # last index is first_index + the length of the expression
            last_index = first_index + len(expression) - 1
    return orig_expression,first_index,last_index

# returns the expression within the outermost parentacees
def find_parantacees(expression):
    forward_par = 0
    back_par = 0
    index = 0
    first_par = -1
    sub_expression = False
    while index<=len(expression):
        if expression[index] == "(":
            forward_par += 1 
            if first_par<0:
                first_par = index
        if expression[index] == ")":
            back_par += 1 
        # if the number forward is equal to the amount back(complete set)
        if forward_par == back_par and forward_par>0:
            # the 'sub_expression' is everything inside those inner/out expressions
            sub_expression = expression[first_par+1:index]
            final_index = index-1 # value of the last element in inner expression
            index = len(expression)+1
        index += 1
    return sub_expression,first_par,final_index

# requires find_no_parantacees to be valid
def eval_wo_par(expression):
    while "!" in expression:
        index = expression.index("!")
        # find the expression containing the "!"
        minimized_list = expression[index-1:index+1]
        result = eval_single_operator(minimized_list)
        expression[index-1] = result
        expression.pop(index)
    # powers go between multiplication and factorial
    while "^" in expression:
        exp_index = expression.index("^")
        minimized_list = expression[exp_index-1:exp_index+2]
        result = eval_single_operator(minimized_list)
        expression[exp_index-1] = result
        expression.pop(exp_index)
        expression.pop(exp_index)
    while "*" in expression or "/" in expression:
        mult_index = -1
        div_index = -1
        if "*" in expression:
            mult_index = expression.index("*")
        if "/" in expression:
            div_index = expression.index("/")
        # if multiplication comes first (and is not -1):
        if (mult_index<div_index and mult_index!=-1) or div_index == -1:
            index = mult_index
        else:
            index = div_index
        minimized_list = expression[index-1:index+2]
        result = eval_single_operator(minimized_list)
        expression[index-1] = result
        expression.pop(index)
        expression.pop(index)
    eval_sub_add(expression)
    return expression[0]

def eval_sub_add(expression):
    while len(expression)!=1:
        expression[0] = eval_single_operator(expression)
        expression.pop(1)
        expression.pop(1)
    return [expression[0]]

def eval_single_operator(express):
    if type(express[0][0] == dict or express[1][0] == dict) and 0:
        print("This expression cannot be calculated due to the location of" +\
             " a non-integer power.")
        raise ValueError
    operator = express[1]
    operator_type = 'normal'
    if len(express)>2:
        if str(express[2]) in "+-/(" and str(express[1]) == "-":
            print("Invalid use of operator: "+str(express[1])+str(express[2]))
            raise ValueError
    if len(express)>2:
        expression = [express[0],express[2]]
        # determine if need to use root operation
        operator_type = determine_operator_type(express[0],express[2])
    # replace these with single functions
    if operator_type == 'normal':
        if operator=="+":
            result = operator_addsub_two(expression,"add")
        elif operator=="-":
            result = operator_addsub_two(expression,"sub")
        elif operator=="*":
            result = operator_mult_two(expression)
        elif operator=="/":
            result = operator_div_two(expression)
        elif operator =="!":
            if type(express[0])==dict:
                # factorial cannot have a 'root' argument
                print("Factorial must be an integer value")
                raise ValueError
            result = operator_factorial(express)
        elif operator == "^":
            # simplify the value into 'root' form 
            result = operator_power(expression)
        else:
            print("'"+str(operator)+"' is an invalid operator.")
            raise ValueError
    else:
        # need to use root operations
        # find the converted values
        val1 = operator_type[0]
        val2 = operator_type[1]
        if operator == "+":
            result = simplifier_root_add(val1,val2,"add")
        elif operator == "-":
            result = simplifier_root_add(val1,val2,"sub")
        elif operator == "*":
            result = simplifier_root_multiply(val1,val2,"mult")
        elif operator == "/":
            result = simplifier_root_multiply(val1,val2,"div")
        elif operator == "^":
            result = operator_power(expression)
    return result

#########################################################################################
#               replace python calculations with functions below                        #
#########################################################################################

def determine_operator_type(val1,val2):
    # if neither are dictionaries
    if type(val1)!=dict and type(val2)!=dict:
        # use 'normal' operators
        return 'normal'
    # if either value is not a dictionary:
    if type(val1)!=dict:
        # convert it to a dictionary
            # key will be "1"
        val1 = {digit_list[1]:[[val1,[digit_list[1],digit_list[1]]]]}
    if type(val2)!=dict:
        val2 = {digit_list[1]:[[val2,[digit_list[1],digit_list[1]]]]}
    # if not 'normal', use root simplification
    return val1,val2

# intended for the multiplication operator
def operator_mult_two(expression_list): # CANNOT CORRECTLY SIMPLIFY
    num1 = expression_list[0][0]
    num2 = expression_list[1][0]
    den1 = expression_list[0][1]
    den2 = expression_list[1][1]
    result_num = calc_multiply(num1,num2)
    result_den = calc_multiply(den1,den2)
    return (simplify([result_num,result_den]))

# intended for the division operator
def operator_div_two(expression_list):
    num1 = expression_list[0][0]
    num2 = expression_list[1][0]
    den1 = expression_list[0][1]
    den2 = expression_list[1][1]
    result_num = calc_multiply(num1,den2)
    result_den = calc_multiply(num2,den1)
    return simplify([result_num,result_den])
    
# intended for the addition and subtraction operators
def operator_addsub_two(expression_list,addsub):
    num1 = expression_list[0][0]
    num2 = expression_list[1][0]
    if addsub == "sub":
        # if the numerator is negative:
        if num2[0] == "-":
            num2 = num2[1:]
            # remove the negative
        else:
            num2 = "-" + num2
            # add a negative
    den1 = expression_list[0][1]
    den2 = expression_list[1][1]
    result_num1 = calc_multiply(num1,den2)
    result_num2 = calc_multiply(num2,den1)
    result_num = det_addsub(result_num1,result_num2)
    result_den = calc_multiply(den1,den2)
    result = [result_num,result_den]
    return simplify(result)

def operator_factorial(expression_list):
    simplify_result = simplify(expression_list[0])
    num = simplify_result[0]
    den = simplify_result[1]
    if den!=digit_list[1] or "-" in num or "-" in den:
        print("Factorial(!) must be a positive integer.")
        raise ValueError
    if num == digit_list[0]:
        return [digit_list[1],den]
    result = digit_list[1]
    while num != digit_list[1]:
        result = calc_multiply(result,num)
        num = calc_add(num,digit_list[1],"sub")
    return [result,den]

# cannot support exponents that are not representable by fractions?
def operator_power(expression_list):
    base = expression_list[0]
    exponent = expression_list[1] # assume is a fraction
    # REMOVE USER ABILITY TO USE FRACTION POWERS
    if(exponent[1]!=digit_list[1]):
        print("Non-integer exponents have been disabled.")
        raise ValueError
    exp_num = exponent[0]
    exp_den = exponent[1]
    if type(base) == list:
        result = base_exponent_simplifier([base,exponent])
    else:
        # while the numerator of the exponent is not 1:
        orig_base = base
        # if the exponent equals zero:
        if exp_num==digit_list[0]:
            # return 1/1
            return [digit_list[1],digit_list[1]]
        # while the exponent's numerator is not 1:
        while exp_num!=digit_list[1]:
            # multiply the base by it's original
            base = simplifier_root_multiply(base,orig_base,"mult")
            # decrease the exponent's numerator by 1
            exp_num = calc_add(exp_num,digit_list[1],"sub")
        result = {exp_den:[[base]]}
    return result

#######################################################################################
###                             exponenets simplification                           ###
# function to convert to decimal form
# when simplifying the exponent expression:
    # remove any negatives from the denominator(put into numerator)


# [[mult_num,mult_den],[base_num,base_den],"^",[exp_num,exp_den]]
# simplifies an expression with "^"
# cannot be used with negative signs (yet)
# reduces to 'root' form

# this function can only be used if there is no addition in the inner root
def simplifyRootWithOneInnerRoot( innerRoot, power ): # created after 126 ended
    ...
    # create a new list of the section under the root
    # convert the power to simplest fraction form
    # for every value in the key of the dictionary (innerRoot keys):
        # multiply that key by the power's denominator (to convert to root form)
        # add that value to the tuple
    # for every value in the value list of the dictionary (innerRoot values):
        # the new value is the original value to the power of the power's numerator
        # append the new value to the new list under the root
    # add the new list as the value of the new key tuple
    # remove the original key from the dictionary
    
def base_exponent_simplifier(expression):
    # expanding into num and den is currently redundant
    if type(expression[1]) != list:
        print("The exponent, "+str(expression[3])+" is irrational.")
    expression[0] = simplify(expression[0])
    expression[1] = simplify(expression[1])
    #expression[3] = simplify(expression[3])
    mult_num = digit_list[1]
    mult_den = digit_list[1]
    base_num = expression[0][0]
    base_den = expression[0][1]
    exp_num = expression[1][0]
    exp_den = expression[1][1]
    # if the exponent numerator is zero, return the multiplier
    if exp_num == digit_list[0]:
        return [mult_num,mult_den]
    # factor out the exponent numerator
    # numerator:
    base_num = power_integer(base_num,exp_num)
    # denominator:
    base_den = power_integer(base_den,exp_num)
    # simplify
    simplify_result_num = simplify_root(mult_num,base_num,exp_den)
    simplify_result_den = simplify_root(mult_den,base_den,exp_den)
    mult_num = simplify_result_num[0]
    base_num = simplify_result_num[1]
    mult_den = simplify_result_den[0]
    base_den = simplify_result_den[1]
    if exp_den == digit_list[1]:
        # return the product of the base and the multiplicator
        return operator_mult_two([[mult_num,mult_den],[base_num,base_den]])
    return {exp_den:[[[mult_num,mult_den],[base_num,base_den]]]}

# takes in 'dictionary form' of a root
# returns in simplified form as a dictionary
# NEEDS TO BE ABLE TO ACCEPT DICTIONARIES
def simplify_root_value(root_value):
    root_val_copy = root_value.copy()
    # for every root_value/root_expression in the root_exp:
    for root_val,root_exp in root_val_copy.items():#######
        # for every subexpression in the root_expression:
        for sub_exp in root_exp:
            # for every base in the subexpression(excluding the multiplier)
            base_index = 1
            for base in sub_exp[1:]:
                # simplily using the correct part of the root_value, root_base, and multiplier
                result = base_exponent_simplifier([sub_exp[0],base,"^",[digit_list[1],root_val]])
                # assign the new multiplier to the old one
                if type(result) == dict:
                    print("OPTION3")
                    root_value[root_val][sub_exp][0] = result[root_val][0][0]
                # if the type is a list
                elif type(result) == list:
                    # if the root_value is a string:
                    if type(root_val)==str:
                        # if there are no other sub_expressions in the expression:
                        if len(root_exp)==1:
                            print("OPTION1")
                            print(root_exp)
                            # RUN THE SIMPLIFY FUNCTION
                            ...
                            # assign the multiplier(list) to root_exp
                            # remove that expression from the dictionary
                            # if '1' is already root value in the dictionary:
                                # add the multipliers together
                            # else:
                                # assign the multiplier to "1" in the dictionary
                # assign the new root_base to the old one
                if type(result) == dict:
                    print("OPTION2")
                    root_value[root_val][sub_exp][base_index] = result[root_val][0][1]
                base_index += 1
    # if the only root_val in the dictionary is "1":
        # return the multiplier
    return root_value

def simplify_root_of_1(root_dict):
    # create a copy
    copy_dict = root_dict.copy()
    # for everything in the copy:
    for root_tuple,root_expression in copy_dict.items():
        index = 0
        # for every root in the tuple of roots:
        for root_val in root_tuple:
            # if the root is equal to 1:
            if root_val == digit_list[1]:
                # multiply the multiplier by the corresponding base
                root_tuple[0] = operator_mult_two([root_tuple[0],root_expression[index+1]])
                # remove the corresponding base from the expression
                root_expression.pop(index+1)
                # remove 1 from the tuple of roots
                root_tuple.remove(root_val)
                

            index += 1
                
                
                

################################################################################################
#                               ROOTS                                                          #
################################################################################################
# when assigning a default value of "1" to expressions without roots, also need a multiplier?
    # "1":[["3","5"],["1","1"]]
# MAKE SURE TO PUT THE MULTIPLIER_ROOT LIST IN ORDER(least => greatest)
    # do not want a ["3","4"] root expression separate from a ["4","3"] root expression
# for 'root' operator:
    # call the simplify_root function:
        # inner_val is the... inner value
        # assume multiplier is ["1","1"] when none is given


### EXAMPLE: simplifier_root_add({"6":[[["3","2"],["5","6"]]],str(["3","4"]):[[["3","5"],["7","9"],["3","1"]]]},{str(["3","4"]):[[["4","1"],["7","9"],["3","1"]],[["1","9"],["15","8"],["9","5"]]],"6":[[["4","3"],["5","6"]]]},"sub")
### simplifies root expressions being added
def simplifier_root_add(val1,val2,addsub):
    # assume val1 is the 'primary' root
        # combine everything from val2 into val1
    # for every root in val2:
    for root_val,properties in val2.items():
        # if that root exists in val1:
        if root_val in val1.keys():
            for root_expression2 in val2[root_val]:
                root_val1_index = 0
                same_bases = False
                for root_expression1 in val1[root_val]:
                    # if all the bases are the same
                    if root_expression1[1:] == root_expression2[1:]:
                        # if the expression is a list:
                        if "]" in root_expression1:
                            mult_simplified = simplify_root_multiplier(root_rep1,root_rep2,addsub)
                            multiplier = mult_simplified[0]
                            bases = root_expression1[1:]
                        # otherwise use direct addition
                        else:
                            # add the multipliers
                            multiplier = operator_addsub_two([root_expression1[0],root_expression2[0]],addsub)
                            # keep everything else constant
                            bases = root_expression1[1]
                            # assign key root_val with the above
                        # only change the multiplier(bases remain constant)
                        val1[root_val][root_val1_index][0] = multiplier
                        same_bases = True
            root_val1_index += 1
            # if the bases are different:
            if not same_bases:
                # add the second value
                # if subtracted:
                if addsub == "sub":
                    if root_expression2[0][0][0] == "-":
                        root_expression2[0][0][0] = root_expression2[0][0][0][1:]
                    # add a negative to the numerator
                    else:
                        root_expression2[0][0] = "-" + root_expression2[0][0]
                val1[root_val].append(root_expression2)
        else:
            # if subtracted,
            if addsub == "sub":
                # add a negative sign to the numerator of the operator
                if val2[root_val][0][0][0][0] == "-":
                    val2[root_val][0][0][0] = val2[root_val][0][0][0][1:]
                else:
                    val2[root_val][0][0][0] = "-"+val2[root_val][0][0][0]#IS THE FIRST 0 HARD-CODED?
            # add that root to val1
            val1[root_val] = properties
    return val1

# also find the multiplier
# ensure the order of the set is from least => greatest'
# EXAMPLE: simplifier_root_multiply({'4': [[['2', '1'], ['4', '1']]]}, {'4': [[['1', '1'], ['4', '1']]]}, "div")
def simplifier_root_multiply(val1,val2,divmult):
    result_dict = {}
    # treat the first as the primary value
    # for every expression in the second value:
    for root2,root_exp2 in val2.items():
        # for every expression in the first value:
        for root1,root_exp1 in val1.items():
            # for every combination of two expressions that contain one multiplier each:
            ####################################
            # iterate for every base_value
            # WILL NEED TO ACCOUNT FOR DICTIONARIES
            for base_values1 in root_exp1:
                for base_values2 in root_exp2:
            ####################################
                    # create a temporary root and multiplier_base set
                    temp_root = ()
                    temp_base = []
                    # calculate and add the multiplier:
                    if divmult == "div":
                        result_mult = operator_div_two([base_values1[0],base_values2[0]])
                    else:
                        result_mult = operator_mult_two([base_values1[0],base_values2[0]])
                    # add the multiplier to the bases
                    temp_base.append(result_mult)
                    # for every root in either one:
                    set_of_roots = set()
                    for root_val in root1:
                        set_of_roots.add(root_val)
                    for root_val in root2:
                        set_of_roots.add(root_val)
                    for root_val in set_of_roots:
                        if root_val in root1:
                            index1 = root1.index(root_val)
                        if root_val in root2:
                            index2 = root2.index(root_val)
                        # if the root is in both:
                        if root_val in root1 and root_val in root2:
                            # assume the mult_base and root are in respective order
                            base1 = base_values1[index1+1] # ensure the multiplier exists 
                            base2 = base_values2[index2+1]    # without a root-reference
                            # multiply the bases together
                            if divmult == "div":
                                base_result = operator_div_two([base1,base2])
                            else:
                                base_result = operator_mult_two([base1,base2])
                        # add the base and root to the temp_set
                        # otherwise:
                        else:
                            # add the existing base and root to the temp_set
                            if root_val in root1:
                                base_result = base_values1[index1+1]
                            else:
                                # swap the num and den when dividing
                                if divmult == "div":
                                    temp_num = base_values2[index2+1][0]
                                    temp_den = base_values2[index2+1][1]
                                    base_values2[index2+1][0] = temp_den
                                    base_values2[index2+1][1] = temp_num
                                base_result = base_values2[index2+1]
                                # if divided:
                        ##### SWAP THE NUM AND DEN OF THE SECOND VALUE BEFORE DIVIDING
                        temp_root += tuple(root_val,)
                        temp_base += [base_result]
            # add the new set
            # if the root is in the dictionary:
            if temp_root in result_dict:
                # append the base onto the previous set of bases
                result_dict[temp_root].append(temp_base)
            else:
                # set the base as a list
                result_dict[temp_root] = [temp_base]
    # return the result
    return result_dict







    



# These elements are added together
# [[mult1_1,base1_1],[mult1_2,base1_2]] , [[mult2_1,base2_1],[mult2_2,base2_2]]]
    # many possible variations
# combine the properties of two values with equal roots (or root lists)
# only call this function without list roots(key)
def combine_root_props_add(prop1,prop2):
    result = {}
    # for any values that are not assigned a dictionary key:
    if type(prop1) != dict:
        # change that property to a dictionary with a root_value = 1 
        prop1 = {digit_list[1]:[prop1]}
        # {"1":all the properties of that root}
    if type(prop2) != dict:
        prop2 = {digit_list[1]:[prop2]}
    # if both are dictionaries of length 1 and share the same root_value:
    if False:#len(prop1) == 1 and len(prop2) == 1:
        # add the values together
        result_dict = [prop1,prop2]
        # assign to result
    else:
        set_of_keys = set()
        for key in prop1.keys():
            set_of_keys.add(key)
        for key in prop2.keys():
            set_of_keys.add(key)
        # for every key that exists in at least one:
        for key in set_of_keys:
            # if key in both properties
            if key in prop1.keys() and key in prop2.keys():
                # call the operator_root_add function
                result_prop = simplifier_root_add({key:prop1[key]},{key:prop2[key]})
                # add that to the result
                result[key] = result_prop[key]
            # else:
            else:
                if key in prop1.keys():
                    result[key] = prop1[key]
                else:
                    result[key] = prop2[key]
                # add the properties of the key that does exist to the result
    return result


# only allows POSITIVE integer bases and exponenets
    # intended to further 'simplify' the simplify_exponenet function
        # can reduct power numerator becomes 1 => (root form)
def power_integer(base,exponent):
    if exponent == digit_list[0]:
        return digit_list[1]
    result_base = digit_list[1]
    while exponent!=digit_list[0]:
        exponent = calc_add(exponent,digit_list[1],"sub")
        result_base = calc_multiply(result_base,base)
    return result_base

# simplifies the "... * ... ^ (1/...)" of an exponent
def simplify_root(outer_value,inner_val,root_val):
    # calculate max_factor
    max_factor = factor_maximum(inner_val)
    root_factor = digit_list[1]
    # for every possible 'root factor':
    while root_factor!=max_factor:
        root_factor = calc_add(root_factor,digit_list[1],"add")
        possible_factor = True
        while possible_factor:
            # calculate the possible factor
            possible_factor = power_integer(root_factor,root_val)
            factor_result = long_division([inner_val,possible_factor],True)
            factor_result = remove_trailing_zeros(factor_result)
            # if the possible_factor is a factor of the inner_val:
            if "." not in factor_result:
                # divide the inner_val by that factor
                inner_val = factor_result
                outer_value = calc_multiply(outer_value,root_factor)
            else:
                possible_factor = False
    #if outer_value == [digit_list[1],digit_list[1]]:
    #    return [inner_val,root_val]
    return [outer_value,inner_val,root_val] # returning root_val is redundant

# EXAMPLE: [[["3","4"],["7","1"],["8","3"]]], \
            #[[["5","3"],["7","4"],["9","3"]],[["3","7"],["7","1"],["8","3"]]],"add")
# adds two root-expressions in 'multiplication format' into one expression
def simplify_root_multiplier(root_rep1,root_rep2,addsub):
    print("root_rep1=",root_rep1)
    print("root_rep2=",root_rep2)
    # treat root_rep1 as the 'official' root_representer
        # 'multiply' values into 2
    # for every combination of root_expressions wrt both representations:
    for mult_expression2 in root_rep2:
        root_added = False
        for mult_expression1 in root_rep1:
            # if the bases are the same for every value(excluding the multiplier)
            if mult_expression1[1:] == mult_expression2[1:]:
                # add the respective multipliers together
                additive_result = operator_addsub_two([mult_expression1[0],mult_expression2[0]],addsub)
                # assign the sum to the multiplier of the corresponding root
                root_rep1[root_rep1.index(mult_expression1)][0] = additive_result
                root_added = True
        # if none of the expressions from were 'root added':
        if not root_added:
            # if subtracted:
            if addsub == "sub":
                # add a negative sign to the numerator of the operator
                mult_expression2[0][0] = "-"+mult_expression2[0][0]
            # directly insert the 2nd expression into the first
            root_rep1.append(mult_expression2)
    return root_rep1

#########################################################################################
#                        base addition/subtraction/multication                          #
#########################################################################################

def calc_add(par1,par2,addsub):
    first = []
    second = []
    for character in par1:
        first.append(character)
    for character in par2:
        second.append(character)
    first.reverse()
    second.reverse()
    if len(first)>len(second):
        longer = first
        shorter = second
    else:
        longer = second
        shorter = first
    result = determine_larger(par1,par2)
    long = result[0]
    short = result[1]
    longer = []
    shorter = []
    for character in long:
        longer.append(character)
    for character in short:
        shorter.append(character)
    longer.reverse()
    shorter.reverse()
    result = []
    # for every character in shorter
    for index in range(len(shorter)):
        short_index = digit_list.index(shorter[index])
        longer_index = digit_list.index(longer[index])
        #################### uses python's decimal addition
        if addsub == 'sub':
            digit_index = longer_index-short_index
        else:
            digit_index = longer_index+short_index
        result.append(digit_index)
    for index in range(len(shorter),len(longer)):
        result.append(digit_list.index(longer[index]))
    result.reverse()
    remove_redundancy(result)
    evaluate_indeces(result)
    return_string = ""
    for element in result:
        return_string += element
    return return_string

        
# indices are hard-coded using decimal
def calc_multiply(val1,val2):
    val1_result = remove_neg(val1)
    val1 = val1_result[0]
    val2_result = remove_neg(val2)
    val2 = val2_result[0]
    negative = (val2_result[1]+val1_result[1])==1
    list1 = []
    list2 = []
    for character in val1:
        list1.append(character)
    for character in val2:
        list2.append(character)
    list1.reverse()
    list2.reverse()
    result = []
    for index1 in range(len(list1)):
        index = 0
        for index2 in range(len(list2)):
            index = index1+index2
            if len(result)<index+1:
                result.append("")

            result[index] = calc_add(result[index],mult_two(list1[index1],list2[index2]),'add')
    for index in range(len(result)):
        #### converted to decimal form for python
#        result[index]= int(result[index])
        result[index]=int(digit_system_to_decimal(result[index]))
    result.reverse()
    result = remove_redundancy(result)
    result = evaluate_indeces(result)
    return "-"*negative + result

def mult_two(val1,val2):
    loc1 = digit_list.index(val1)
    loc2 = digit_list.index(val2)
    result = digit_list[0]
    for iteration in range(loc1):
        result = calc_add(result,val2,'add')
    return_string = ""
    for element in result:
        return_string += element
    return return_string

def split_by_decimal(element):
    
    if "." in element:
        index = element.index(".")
        greater = element[:index]
        lesser = element[index+1:]
        if greater == "":
            greater = digit_list[0]
        if lesser == "":
            lesser = digit_list[0]
    else:
        greater = element
        lesser = digit_list[0]
    if "." in greater or "." in lesser:
        print("There are multiple decimals in a single value")
        raise ValueError
    return greater,lesser

# puts a single function into non-decimal fraction form
def split_by_slash(element):
    if "/" in element:
        index = element.index("/")
        numerator = element[:index]
        denominator = element[index+1:]
        if denominator == "":
            denominator = digit_list[1]
    else:
        numerator = element
        denominator = digit_list[1]
    if "/" in numerator or "/" in denominator:
        print("There are multiple decimals in a single value")
        raise ValueError
    return [numerator,denominator]

def remove_decimal(element_list):
    numerator = element_list[0]
    denominator = element_list[1]
    while "." in element_list[0] or "." in element_list[1]:
        for numden in element_list:
            if "." in numden:
                index = numden.index(".")
                numden = numden[:index]+numden[index+1]+"."+numden[index+2:]
                if numden[-1]==".":
                    numden = numden[:-1]
            else:
                numden += digit_list[0]
        for index2 in range(len(element_list)):
            numden = element_list[index2]
            if "." in numden:
                index = numden.index(".")
                numden = numden[:index]+numden[index+1]+"."+numden[index+2:]
                if numden[-1]==".":
                    numden = numden[:-1]
            else:
                numden += digit_list[0]
            element_list[index2] = numden
    # simplify the fracetion
    element_list = simplify(element_list)
    return [element_list[0],element_list[1]]

def remove_redundancy(list_of_digits):
    list_of_digits.reverse()
    for index in range(len(list_of_digits)):
        # while the index is greater than the value of the maximum digit:
        while list_of_digits[index]>=len(digit_list):
            # subtract the length of the digit_list from the current index
            list_of_digits[index] -= len(digit_list)
            # add an extra element if there is not one already
            if index+1==len(list_of_digits):
                list_of_digits.append(0)
            # increase the value of the next index by 1
            list_of_digits[index+1] += 1
        # while the index is under zero
        while list_of_digits[index]<0:
            # increase the index by len(digit_list)
            list_of_digits[index] += len(digit_list)
            # decrease the 'larger' element(WRT list_of_digits) by 1
            list_of_digits[index+1] -= 1
            # the largest value will not be negative(don't need to append)
    list_of_digits.reverse()
    return list_of_digits

def digit_system_to_decimal(string_element):
    decimal = 0
    counter = 0
    while len(string_element)>0:
        remainder = string_element[-1]
        remainder_index = digit_list.index(remainder)
        string_element = string_element[:-1]
        decimal += remainder_index * len(digit_list) ** counter
        counter += 1
    return decimal


        
def decimal_to_digit_system(dec_value):
    dec_value = int(dec_value)
    # find the maximum length of the result
    result_length = math.ceil(dec_value**(1/len(digit_list)))
    result = [digit_list[0]]*result_length
    # for every element in result:
    for element_index in range(result_length):
        # while a representative digit-value of '1' can be subtracted from dec_value
        while dec_value>=(len(digit_list)**(result_length-element_index-1)):
            # sutract that representative value from dec_value
            dec_value -= (len(digit_list)**(result_length-element_index-1))
            # increase the element in the respective digit by 1
            result[element_index] = calc_add(result[element_index],digit_list[1],"add")
    result_string = ""
    for value in result:
        result_string += value
    return result_string

            
        


    
            
def evaluate_indeces(list_of_indices):
    for index in range(len(list_of_indices)):
        list_of_indices[index] = digit_list[list_of_indices[index]]
    return_string = ""
    for element in list_of_indices:
        return_string += element
    return return_string
    return list_of_indices

def det_addsub(val1,val2):
    if val1[0] == "-" and val2[0] == "-":
        addsub = "add"
    elif val1[0] != "-" and val2[0] != "-":
        addsub = "add"
    else:
        addsub = "sub"
    pos1 = True
    pos2 = True
    if val1[0] == "-":
        val1 = val1[1:]
        pos1 = False
    if val2[0] == "-":
        val2 = val2[1:]
        pos2 = False
    if len(val1)>len(val2):
        longer = val1
        shorter = val2
    # if lengths are equal:
    elif len(val1)==len(val2):
        # determine which has a larger magnitude
        cur_index = 0
        if val1!=val2:
            while val1[cur_index]==val2[cur_index]:
                cur_index += 1
        else:
            # order does not matter
            cur_index = 0
        if digit_list.index(val1[cur_index])>digit_list.index(val2[cur_index]):
            longer = val1
            shorter = val2
        else:
            longer = val2
            shorter = val1
    else:
        longer = val2
        shorter = val1
    # if the longer value is positive, result is positive
    if (val1 == longer and pos1) or (val2 == longer and pos2):
        negative = False
    else:
        negative = True
    result = calc_add(longer,shorter,addsub)
    return "-"*negative+result

# currently only simplifies if numerator is greater than denominator
def simplify(element_list):
    num = element_list[0]
    num = remove_trailing_zeros(num)
    orig_num = num
    den = element_list[1]
    num_result = remove_neg(num)
    num = remove_trailing_zeros(num_result[0])
    den_result = remove_neg(den)
    den = remove_trailing_zeros(den_result[0])
    negative = (den_result[1]+num_result[1])==1
    factors = 0
    #factor_value = digit_list[2]
    factor_value = calc_add(digit_list[1],digit_list[1],"add")
    # shortcuts
    if den == digit_list[1]: # No simplification if den is 1
        return [negative*"-"+num,den]
    if num == digit_list[1]: # No simplification if num is 1
        return [negative*"-"+num,den]
    if den == digit_list[0]:
        print("Divide by 0.")
        raise ValueError
    ##########
    large_small = determine_larger(num,den)
    num_holder = num
    den_holder = den
    # treat the larger value as the numerator
    num = large_small[0]
    den = large_small[1]
    swapped = num != num_holder
    ########
    # orig_num can be lowered up to the sqrt(orin_num)
    # create function to find the greatest factor
    factor_max = factor_maximum(num)
    while factor_value != factor_max:
        # there may be more factors
        more_factors = True
        # while there may be more factors:
        while more_factors:
            # find the result of long_division (num/den) and (den/num)
            # remove zeros and unecessary decimals
            num_factored = long_division([num,factor_value],True)
            den_factored = long_division([den,factor_value],True)
            num_factored = remove_trailing_zeros(num_factored)
            den_factored = remove_trailing_zeros(den_factored)
            # if there is a decimal in either result:
            if "." in num_factored or "." in den_factored or num==num_factored:
                more_factors = False
                # there may be more factors is false
            else:
                # the numerator becomes the result of long_division
                num = num_factored
                # the denominator becomes the result of long_division
                den = den_factored
                # there may be more factors remains true
        factor_value = calc_add(factor_value,digit_list[1],"add")
    ###############
    # if the order was swapped:
    if swapped:
        # swap the order again
        num_holder = num
        den_holder = den
        num = den_holder
        den = num_holder
    ###############
    # return the new numerator and denominator
    #print("End of the 'simplification'.\n")
    return [negative*"-"+num,den]

# the greatest possible factor is sqrt(value) (take last half of numbers)
def factor_maximum(value):
    value = value[(len(value)-1)//2:]
    if value[0] == digit_list[0]:
        value = digit_list[1]+value
    return value

# I REMOVED THE "not for_factors*(index>=len_of_orig_num)"
def long_division(element_list,for_factors):
    if element_list[0] == digit_list[0]:
        return digit_list[0]
    pre_digits = True
    leading_zeros = 0
    num = element_list[0]
    den = element_list[1]
    num_result = remove_neg(num)
    num = num_result[0]
    den_result = remove_neg(den)
    den = den_result[0]
    negative = (den_result[1]+num_result[1])==1
    if den == digit_list[1]:
        return "-"*negative + num
    if den == digit_list[0] or len(den)==0:
        print("Divide by 0.")
        raise ValueError
    len_of_orig_num = len(num)
    # add zeros to make the length of num equal to accuracy
    num += digit_list[0]*(ACCURACY-len(num))
    result = [digit_list[0]]*ACCURACY
    index = -1
    num_equals_zero = False
    # the loop continues 1 more time for every leading zero
    # if for factors: only run while index is less than length of orig_num_list
    while index<ACCURACY + leading_zeros -1 and not num_equals_zero:
        #########################
        # if the function is only to determine factors:
        if for_factors:
            # if the index is past the decimal:
            if index>len_of_orig_num:
                # return a decimal value(not a valid factor)
                return ".1"
        #########################
        index += 1
        # while the denominator can be factored out of the numerator WRT the index
        rel_value = den + digit_list[0]*(ACCURACY+leading_zeros-index-1)
        large_small = determine_larger(num,rel_value)
        larger = large_small[0]
        # while num is the larger value:
        while larger == num:
            # subtract den plus digit_list[0]*(index_WRT decimal)
            rel_value = den + digit_list[0]*(ACCURACY+leading_zeros-index-1)
            # use a relative value to represent the value of the denominator WRT num
            num = calc_add(num,rel_value,"sub") 
            # add digit_list[1] plus the "digit_list[0]"s to the result
            num = remove_leading_zeros(num)
            result[index] = calc_add(result[index],digit_list[1],"add")
            # if the numerator is zero, stop calculating
            if digit_system_to_decimal(num) == 0:
                result_string = ""
                counter = 0
                for element in result:
                    if counter == len_of_orig_num:
                        result_string += "."
                    result_string += element
                    counter += 1
                return "-"*negative + result_string
            large_small = determine_larger(num,rel_value)
            larger = large_small[0]
        # if a 'pre_digit' is equal to 0
        if result[index] == digit_list[0] and pre_digits:
            # add an additional digit to the end result
            leading_zeros += 1
            num += digit_list[0]
            result += digit_list[0]
        else:
            pre_digits = False
        for character in num:
            if character != 0:
                num_equals_zero = False
        
        
    result_string = ""
    counter = 0
    for element in result:
        if counter == len_of_orig_num:
            result_string += "."
        result_string += element
        counter += 1
    return "-"*negative + result_string
   
def determine_larger(val1,val2):
    val1 = remove_leading_zeros(val1)
    val2 = remove_leading_zeros(val2)
    if val1 == digit_list[0]:
        if val2 == digit_list[0]:
            return digit_list[0],digit_list[0]
        return val2,digit_list[0]
    if val2 == "":
        return val1,digit_list[0]
    if len(val1)>len(val2):
        longer = val1
        shorter = val2
    # if lengths are equal:
    elif len(val1)==len(val2):
        # determine which has a larger magnitude
        cur_index = 0
        if val1!=val2:
            while val1[cur_index]==val2[cur_index]:
                cur_index += 1
        else:
            # order does not matter
            cur_index = 0
        if digit_list.index(val1[cur_index])>digit_list.index(val2[cur_index]):
            longer = val1
            shorter = val2
        else:
            longer = val2
            shorter = val1
    else:
        longer = val2
        shorter = val1
    return [longer,shorter]

def remove_leading_zeros(element):
    if element == "":
        return digit_list[0]
    while element[0] == digit_list[0]:
        element = element[1:]
        if len(element) == 0:
            return digit_list[0]
    if element == "":
        element = digit_list[0]
    return element

# This function should not need to be very long. 
def remove_trailing_zeros(element):
    if len(element)!=1:
        if element[0] == "-":
            negative = True
            element = element[1:]
        else:
            negative = False
    else:
        return element
    if "." in element:
        rev_element = ""
        for index in range(len(element)):
            rev_element += element[len(element)-index-1]
        while rev_element[0] == digit_list[0]:
            rev_element = rev_element[1:]
            if rev_element == "":
                return ""
        if rev_element[0] == ".":
            rev_element = rev_element[1:]
        element = ""
        for index in range(len(rev_element)):
            element += rev_element[len(rev_element)-index-1]
    element = remove_leading_zeros(element)
    return negative*"-" + element

def remove_neg(value):
    if len(value)==0:
        return [value,False]
    else:
        if value[0] == "-":
            value = value[1:]
            negative = True
        else:
            negative = False
        return [value,negative]

main()


