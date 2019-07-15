from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Patrons, Authors, Books, Genres

engine = create_engine('sqlite:///librarycatalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

patron1 = Patrons(name='Duncan Kraus')
session.add(patron1)
session.commit()

patron2 = Patrons(name='Beatrice Beran')
session.add(patron2)
session.commit()

patron3 = Patrons(name='Lex Killough')
session.add(patron3)
session.commit()

print "patrons added"

author1 = Authors(name='J.K. Rowling', book_count=7)
session.add(author1)
session.commit()

author2 = Authors(name='Becky Albertalli', book_count=2)
session.add(author2)
session.commit()

author3 = Authors(name='Gillian Flynn', book_count=1)
session.add(author3)
session.commit()

author4 = Authors(name='Toni Morrison', book_count=3)
session.add(author4)
session.commit()

author5 = Authors(name='Daniel Heath Justice', book_count=1)
session.add(author5)
session.commit()

print "Authors added"

genre1 = Genres(name='Fantasy')
session.add(genre1)
session.commit()

genre2 = Genres(name='Young Adult')
session.add(genre2)
session.commit()

genre3 = Genres(name='Thriller')
session.add(genre3)
session.commit()

genre4 = Genres(name='Magic Realism')
session.add(genre4)
session.commit()

genre5 = Genres(name='African-American Literature')
session.add(genre5)
session.commit()

print "Genres added"

book1 = Books(title="Harry Potter and the Philosopher's Stone", genre=genre1, summary="The first novel in the Harry Potter series and Rowling's debut novel, it follows Harry Potter, a young wizard who discovers his magical heritage on his eleventh birthday, when he receives a letter of acceptance to Hogwarts School of Witchcraft and Wizardry. Harry makes close friends and a few enemies during his first year at the school, and with the help of his friends, Harry faces an attempted comeback by the dark wizard Lord Voldemort, who killed Harry's parents, but failed to kill Harry when he was just 15 months old.", authors=author1, patrons=patron1)
session.add(book1)
session.commit()

book2 = Books(title="Harry Potter and the Chamber of Secrets", genre=genre1, summary="The second novel in the Harry Potter series. The plot follows Harry's second year at Hogwarts School of Witchcraft and Wizardry, during which a series of messages on the walls of the school's corridors warn that the Chamber of Secrets has been opened and that the heir of Slytherin would kill all pupils who do not come from all-magical families. These threats are found after attacks which leave residents of the school petrified. Throughout the year, Harry and his friends Ron and Hermione investigate the attacks.", authors=author1)
session.add(book2)
session.commit()

book3 = Books(title="Harry Potter and the Prisoner of Azkaban", genre=genre1, summary="The third in the Harry Potter series. The book follows Harry Potter, a young wizard, in his third year at Hogwarts School of Witchcraft and Wizardry. Along with friends Ronald Weasley and Hermione Granger, Harry investigates Sirius Black, an escaped prisoner from Azkaban who they believe is one of Lord Voldemort's old allies.", authors=author1, patrons=patron3)
session.add(book3)
session.commit()

book4 = Books(title="Harry Potter and the Goblet of Fire", genre=genre1, summary="The fourth novel in the Harry Potter series. It follows Harry Potter, a wizard in his fourth year at Hogwarts School of Witchcraft and Wizardry and the mystery surrounding the entry of Harry's name into the Triwizard Tournament, in which he is forced to compete.", authors=author1)
session.add(book4)
session.commit()

book5 = Books(title="Harry Potter and the Order of the Phoenix", genre=genre1, summary="The fifth novel in the Harry Potter series. It follows Harry Potter's struggles through his fifth year at Hogwarts School of Witchcraft and Wizardry, including the surreptitious return of the antagonist Lord Voldemort, O.W.L. exams, and an obstructive Ministry of Magic.", authors=author1)
session.add(book5)
session.commit()

book6 = Books(title="Harry Potter and the Half-Blood Prince", genre=genre1, summary="The sixth and penultimate novel in the Harry Potter series. Set during protagonist Harry Potter's sixth year at Hogwarts, the novel explores the past of Harry's nemesis, Lord Voldemort, and Harry's preparations for the final battle against Voldemort alongside his headmaster and mentor Albus Dumbledore.", authors=author1)
session.add(book6)
session.commit()

book7 = Books(title="Harry Potter and the Deathly Hallows", genre=genre1, summary="The seventh and final novel of the Harry Potter series.", authors=author1)
session.add(book7)
session.commit()

book8 = Books(title="Simon vs. the Homo Sapiens Agenda", genre=genre2, summary="This coming-of-age story focuses on its titular protagonist Simon Spier, a closeted gay high-school aged boy who is forced to come out after a blackmailer discovers Simon's e-mails written to another closeted classmate with whom he has fallen in love.", authors=author2, patrons=patron2)
session.add(book8)
session.commit()

book9 = Books(title="Leah on the Offbeat", genre=genre2, summary="Leah on the Offbeat focuses on Leah, the best friend of Simon Spier, and her attempts to deal with various personal issues including friendships and relationships, body image, sexuality, self-esteem, going to college and feeling like an outsider.", authors=author2)
session.add(book9)
session.commit()

book10 = Books(title="Gone Girl", genre=genre3, summary="In Carthage, Mo., former New York-based writer Nick Dunne and his glamorous wife Amy present a portrait of a blissful marriage to the public. However, when Amy goes missing on the couple's fifth wedding anniversary, Nick becomes the prime suspect in her disappearance. The resulting police pressure and media frenzy cause the Dunnes' image of a happy union to crumble, leading to tantalizing questions about who Nick and Amy truly are.", authors=author3)
session.add(book10)
session.commit()

book11 = Books(title="Beloved", genre=genre4, summary="Beloved begins in 1873 in Cincinnati, Ohio, where the protagonist Sethe, a former slave, has been living with her eighteen-year-old daughter Denver. Sethe's mother-in-law, Baby Suggs lived with them until her death eight years earlier. Just before Baby Suggs' death, Sethe's two sons, Howard and Buglar, had run away. Sethe believes they fled because of the malevolent presence of an abusive ghost that haunted their house at 124 Bluestone Road for years.", authors=author4)
session.add(book11)
session.commit()

book12 = Books(title="Song of Solomon", genre=genre5, summary="Song of Solomon follows the life of Macon 'Milkman' Dead III, an African-American man living in Michigan, from birth to adulthood.", authors=author4)
session.add(book12)
session.commit()

book13 = Books(title="The Bluest Eye", genre=genre5, summary="The novel, which takes place in Lorain, Ohio, tells the life of a young African-American girl named Pecola who grows up during the years following the Clutch Plague.", authors=author4)
session.add(book13)
session.commit()

book14 = Books(title="The Way of Thorn and Thunder", genre=genre1, summary="Taking genre1 literature beyond the stereotypes, Daniel Heath Justice's acclaimed Thorn and Thunder novels are set in a world resembling eighteenth-century North America. The original trilogy is available here for the first time as a fully revised one-volume novel. The story of the struggle for the green world of the Everland, home of the forest-dwelling Kyn, is an adventure tale that bends genre and gender.", authors=author5)
session.add(book14)
session.commit()

print "Books added"
print "All done!"
