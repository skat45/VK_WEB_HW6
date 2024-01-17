from itertools import islice
from django.core.management.base import BaseCommand
from random import choice
from ...models import *
from faker import Faker

faker = Faker()


class Command(BaseCommand):

    help = 'This command need to fill data base with faker lib'

    # How many arguments and which command must get
    def add_arguments(self, parser):
        parser.add_argument("-r", "--ratio", type=int)

    def handle(self, *args, **options):
        ratio = None

        try:
            ratio = options["ratio"]
        except:
            pass

        if not ratio:
            if str(input('Ratio number is empty. Shall you use default ration = 10 000? [y/N] ')).lower() == 'y':
                ratio = 10000
                """
                    If you use default ration = 10.000, you have:

                    * 10.001 users
                    * 100.001 questions
                    * 1.000.001 answers
                    * 1.000.001 likes to questions
                    * 1.000.001 likes to answers
                      Summary more than 2M likes by users
                    * 10.001 tags            
                """

        if ratio:
            print('Creating users...')
            # self.fill_users(ratio + 1)
            print('Creating tags...')
            # self.fill_tags(ratio + 1)
            print('Creating questions...')
            # self.fill_questions(ratio * 10 + 1)
            print('Creating answers to questions...')
            # self.fill_answers(ratio * 100 + 1)
            print('Creating likes to questions...')
            self.fill_likes_on_question(ratio * 100 + 1)
            print('Creating likes to answers...')
            self.fill_likes_on_answer(ratio * 100 + 1)
            print('Done!')

    def fill_questions(self, n):
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        tags = list(
            Tag.objects.values_list(
                "id", flat=True
            )
        )

        for i in range(n):
            question = Question.objects.create(author_id=choice(users),
                                               title=faker.sentence()[:128],
                                               text=". ".join(faker.sentences(faker.random_int(min=2, max=5))),
                                               date=faker.date_between("-100d", "today"))
            tag1 = choice(tags)
            tag2 = choice(tags)
            while tag1 == tag2:
                tag2 = choice(tags)
            question.tags.add(tag1)
            question.tags.add(tag2)

    def fill_answers(self, n):
        questions = list(
            Question.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        answers = []

        for i in range(n):
            answer = Answer(question_id=choice(questions),
                            author_id=choice(users),
                            text=". ".join(faker.sentences(faker.random_int(min=2, max=5))))
            answers.append(answer)

        batch_size = 100000
        while True:
            batch = list(islice(answers, batch_size))
            del answers[:batch_size]
            if not batch:
                break
            Answer.objects.bulk_create(batch, batch_size)

    def fill_users(self, n):
        usernames = set()

        while len(usernames) != n:
            usernames.add(faker.user_name() + str(faker.random.randint(0, 1000000)))

        for name in usernames:
            user = User.objects.create(username=name, password=faker.password(), email=faker.email())
            Profile.objects.create(user=user, login=faker.name())

    def fill_tags(self, n):
        for i in range(n):
            Tag.objects.create(name=faker.word(), rating=faker.random.randint(0, 255))

    def fill_likes_on_question(self, n):
        questions = list(
            Question.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        likes = []
        for i in range(n):
            like = LikeToQuestion(question_id=choice(questions), user_id=choice(users),
                                  is_liked=faker.random.randint(-1, 1))
            question = Question.objects.get(id=like.question_id)
            question.rating += like.is_liked
            question.save()
            likes.append(like)

        batch_size = 100000
        while True:
            batch = list(islice(likes, batch_size))
            del likes[:batch_size]
            if len(batch) == 0:
                break
            LikeToQuestion.objects.bulk_create(batch, batch_size)

    def fill_likes_on_answer(self, n):
        answers = list(
            Answer.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        likes = []
        for i in range(n):
            like = LikeToAnswer(answer_id=choice(answers), user_id=choice(users),
                                is_liked=faker.random.randint(-1, 1))
            answer = Answer.objects.get(id=like.answer_id)
            answer.rating += like.is_liked
            answer.save()
            likes.append(like)

        batch_size = 10000
        while True:
            batch = list(islice(likes, batch_size))
            del likes[:batch_size]
            if len(batch) == 0:
                break
            LikeToAnswer.objects.bulk_create(batch, batch_size)
