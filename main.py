from forms import Question


def map_question(label, question_list):
	for index, item in enumerate(question_list):
		if label == item.label:
			return question_list.pop(index)
	print(f'Couldn\'t map question "{label}"')


def cast_value_for_other(cell_value, categories):
	other_count = 0
	for cat in categories:
		if cat.is_other:
			other_count += 1
		else:
			cell_value = cell_value.replace(cat.label, '')
	for i in cell_value.strip(' ,').split(',', other_count):
		yield i.strip(' ,')


def write_form_data_to_xlsx(worksheet, form_data, questionnaire):
	col_offset = 0
	header_row = 1
	category_row = header_row + 1
	row_initial_offset = category_row + 1
	col_initial_offset = 1
	question_list = [i for i in questionnaire.questions]
	for col_num, title in enumerate(form_data[0]):
		question = map_question(title, question_list)
		worksheet.cell(header_row, col_num + col_initial_offset + col_offset).value = title

		# print(f'Writing "{header}"...')
		for row_num, row in enumerate(form_data[1:]):
			if question and question.categories:
				if question.has_other:
					other_values_reversed = cast_value_for_other(row[col_num], question.categories)
				for cat_index, cat in enumerate(question.categories):
					current_column = col_num + col_initial_offset + col_offset + (cat_index if question.q_type == Question.MULTIPLE else 0)
					if question.q_type == Question.MULTIPLE:
						worksheet.cell(category_row, current_column).value = cat.label
					if cat.is_other:
						other_value = next(other_values_reversed)
						if other_value:
							worksheet.cell(row_num + row_initial_offset, current_column).value = cat.code
							worksheet.cell(category_row, current_column + 1).value = cat.label
							worksheet.cell(row_num + row_initial_offset, current_column + 1).value = other_value
					elif cat.label in row[col_num]:
						worksheet.cell(row_num + row_initial_offset, current_column).value = cat.code
			else:
				try:
					worksheet.cell(row_num + row_initial_offset, col_num + col_initial_offset + col_offset).value = row[col_num]
				except IndexError:
					pass
		try:
			if question.q_type == Question.MULTIPLE:
				col_offset += sum(2 if i.is_other else 1 for i in question.categories) - 1
			elif question.q_type == Question.SINGLE:
				col_offset += 0
			elif question.q_type == Question.TEXT:
				col_offset += 0
		except AttributeError:
			pass


def write_questionnaire_to_xlsx(worksheet, questionnaire):
	for question in questionnaire.questions:
		worksheet.append([question.label, question.q_type])
		for category in question.categories:
			worksheet.append([category.code, category.label, '[open]' if category.is_other else None])
