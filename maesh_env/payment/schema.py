import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from payment.models import Transaction

# Create a GraphQL type for the Transaction model
class TransactionType(DjangoObjectType):
	class Meta:
		model = Transaction

# Create a Query type
class Query(ObjectType):
	transaction = graphene.Field(TransactionType, id=graphene.Int())
	transactions = graphene.List(TransactionType)

	def resolve_transaction(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Transaction.objects.get(pk=id)

		return None

	def resolve_transactions(self, info, **kwargs):
		return Transaction.objects.all()

# Create Input Object Types
class TransactionInput(graphene.InputObjectType):
	id = graphene.ID()
	amount = graphene.Float()
	currency = graphene.String() # max_length =3
	UEN = graphene.String() # max_length=10
	companyName = graphene.String()
	redirectUri = graphene.String()
	referenceCode = graphene.String()
	transactionID = graphene.String()

# Create mutations for transactions
class CreateTransaction(graphene.Mutation):
	class Arguments:
		input = TransactionInput(required=True)

	ok = graphene.Boolean()
	transaction = graphene.Field(TransactionType)

	@staticmethod
	def mutate(root, info, input=None):
		ok = True
		transaction_instance = Transaction(amount=input.amount,currency=input.currency,UEN=input.UEN,company_name=input.companyName,redirect_uri=input.redirectUri,reference_code=input.referenceCode)
		transaction_instance.save()
		return CreateTransaction(ok=ok, transaction=transaction_instance)

class UpdateTransaction(graphene.Mutation):
	class Arguments:
		id = graphene.Int(required=True)
		input = TransactionInput(required=True)

	ok = graphene.Boolean()
	transaction = graphene.Field(TransactionType)

	@staticmethod
	def mutate(root, info, id, input=None):
		ok = False
		transaction_instance = Transaction.objects.get(pk=id)
		if transaction_instance:
			ok = True
			transaction_instance.amount = input.amount
			transaction_instance.save()
			return UpdateTransaction(ok=ok, transaction=transaction_instance)
		return UpdateTransaction(ok=ok, transaction=None)

class Mutation(graphene.ObjectType):
	create_transaction = CreateTransaction.Field()
	update_transaction = UpdateTransaction.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)