# Определяем класс Tag, это отновной класс в данном модуле, остальные будет на его основе
# Чтобы не трогать инит в HTML я присваимаю тэгу его имя
class Tag:
    def __init__(self, tag = 'tag', is_single = False, output=None, **attris):
        self.tag = tag
        self.text = ""
        self.attributes = attris
        self.children = []
        self.is_Child_Tag = False    # флаг дочернего тега
        self.is_single = is_single   # флаг одиночного тега
        self.output = output

    def __enter__(self):
        return self

    def __exit__(self, *args): # Был вариан экситу сделать пасс и переопределить его только в HTML, но так получилось сделать рабочим
        if self.is_Child_Tag is False:  # Выполняется только если тег не дочерний
            childs = ""
            for child in self.children:
                childs += str(child)
            if self.is_single:
                print("<{tag} {attrs}>".format(tag=self.tag, attrs=self.tag_attrebutes()))
            else:
                print("<{tag} {attrs}>{text}{childs}</{tag}>".format(tag=self.tag, attrs=self.tag_attrebutes(), text=self.text, childs=childs))

    def __add__(self, other):
        other.is_Child_Tag = True   #Включаем флаг дочке
        self.children.append(other)
        return self    

    def __str__(self):
        if self.children:
            childs = ""
            for child in self.children:
                childs += str(child)
            return "<{tag} {attrs}>{text}{childs}</{tag}>".format(
                tag=self.tag, attrs=self.tag_attrebutes(), text=self.text, childs=childs
            )
        else:
            if self.is_single:
                return "<{tag} {attrs}>".format(
                    tag=self.tag, attrs=self.tag_attrebutes()
                )
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=self.tag_attrebutes(), text=self.text
                )

    def tag_attrebutes(self): #приводим атрибут в нужный вид(это вариант 2 через функцию) 
        if self.attributes:
            attrs = " "
            for attribute, value in self.attributes.items():
                if attribute =="klass":
                    attribute = "class"
                    temp_value = ""
                    for i in value:
                        temp_value += i + " "
                    value = temp_value[0:-1]
                attrs += f'{attribute}="{value}" '
            return attrs[0:-1]
        else:
            return ''


class TopLevelTag(Tag): # не понял для чего класс топлевел, поэтому просто он копия класса Tag
    pass

class HTML(Tag): # В этом классе переопределяем вывод, на выбор в файл если задано имя файла или в консоль если не задано
    def __enter__(self):
            return self

    def __exit__(self, *args):
        childs = ''
        for child in self.children:
            childs += str(child)
        if self.output is not None:
            f = open(self.output, "w")
            f.write(f'<html{self.tag_attrebutes()}>{childs}</html>')
            f.close()

        else:
            print(f'<html{self.tag_attrebutes()}>{childs}</html>')

# Вариант HTML до напильника и выноса атрибутов в функцию
# class HTML(Tag):
#     def __init__(self, tag = "HTML", output='', *args, **kwargs):
#         self.tag = tag
#         self.output = output
#         self.attributes = {}
#         self.children = []

#     def __enter__(self):
#             return self

#     def __exit__(self, *args):
#         childs = ''
#         for child in self.children:
#             childs += str(child)
#         attrs = []
#         for attribute, value in self.attributes.items():
#             attrs.append('%s="%s"' % (attribute, value))
#         attrs = " ".join(attrs)
#         if self.output:
#             with open(self.output, 'w') as f:
#                 print("<{tag} {attrs}>{childs}</{tag}>".format(tag=self.tag, attrs=attrs, childs=childs), file=f)
#         else:
#             print("<{tag} {attrs}>{childs}</{tag}>".format(tag=self.tag, attrs=attrs, childs=childs))

