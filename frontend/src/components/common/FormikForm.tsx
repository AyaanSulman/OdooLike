import React from 'react';
import { Formik, Form, Field, ErrorMessage, FormikHelpers, FormikProps } from 'formik';
import * as Yup from 'yup';
import {
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  Checkbox,
  FormControlLabel,
  Box,
  Typography,
  Divider,
  Paper,
} from '@mui/material';

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'checkbox' | 'textarea' | 'date';
  placeholder?: string;
  options?: Array<{ value: string | number; label: string }>;
  required?: boolean;
  validation?: any;
  gridProps?: { xs?: number; sm?: number; md?: number; lg?: number };
  multiline?: boolean;
  rows?: number;
  disabled?: boolean;
}

interface FormSectionProps {
  title?: string;
  fields: FormField[];
}

interface FormikFormProps {
  initialValues: Record<string, any>;
  onSubmit: (values: any, formikHelpers: FormikHelpers<any>) => void | Promise<any>;
  validationSchema?: Yup.ObjectSchema<any>;
  sections: FormSectionProps[];
  submitButtonText?: string;
  cancelButtonText?: string;
  onCancel?: () => void;
  loading?: boolean;
  error?: string | null;
}

const FormikForm: React.FC<FormikFormProps> = ({
  initialValues,
  onSubmit,
  validationSchema,
  sections,
  submitButtonText = 'Submit',
  cancelButtonText = 'Cancel',
  onCancel,
  loading = false,
  error = null,
}) => {
  const renderField = (field: FormField, formikProps: FormikProps<any>) => {
    const { values, errors, touched, handleChange, handleBlur, setFieldValue } = formikProps;
    const hasError = touched[field.name] && Boolean(errors[field.name]);
    const errorMessage = touched[field.name] && errors[field.name];

    switch (field.type) {
      case 'select':
        return (
          <FormControl fullWidth error={hasError} disabled={field.disabled}>
            <InputLabel id={`${field.name}-label`}>{field.label}</InputLabel>
            <Field
              as={Select}
              labelId={`${field.name}-label`}
              id={field.name}
              name={field.name}
              value={values[field.name] || ''}
              label={field.label}
              onChange={handleChange}
              onBlur={handleBlur}
            >
              {field.options?.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Field>
            {hasError && <FormHelperText>{errorMessage as string}</FormHelperText>}
          </FormControl>
        );

      case 'checkbox':
        return (
          <FormControlLabel
            control={
              <Checkbox
                checked={values[field.name] || false}
                onChange={handleChange}
                name={field.name}
                color="primary"
                disabled={field.disabled}
              />
            }
            label={field.label}
          />
        );

      case 'textarea':
        return (
          <TextField
            fullWidth
            id={field.name}
            name={field.name}
            label={field.label}
            value={values[field.name] || ''}
            onChange={handleChange}
            onBlur={handleBlur}
            error={hasError}
            helperText={errorMessage as string}
            placeholder={field.placeholder}
            multiline
            rows={field.rows || 4}
            variant="outlined"
            disabled={field.disabled}
          />
        );

      case 'date':
        return (
          <TextField
            fullWidth
            id={field.name}
            name={field.name}
            label={field.label}
            type="date"
            value={values[field.name] || ''}
            onChange={handleChange}
            onBlur={handleBlur}
            error={hasError}
            helperText={errorMessage as string}
            InputLabelProps={{ shrink: true }}
            disabled={field.disabled}
          />
        );

      default:
        return (
          <TextField
            fullWidth
            id={field.name}
            name={field.name}
            label={field.label}
            type={field.type}
            value={values[field.name] || ''}
            onChange={handleChange}
            onBlur={handleBlur}
            error={hasError}
            helperText={errorMessage as string}
            placeholder={field.placeholder}
            multiline={field.multiline}
            rows={field.rows}
            variant="outlined"
            disabled={field.disabled}
          />
        );
    }
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
      enableReinitialize
    >
      {(formikProps) => (
        <Form>
          {error && (
            <Box sx={{ mb: 2 }}>
              <Typography color="error">{error}</Typography>
            </Box>
          )}

          {sections.map((section, sectionIndex) => (
            <Paper
              key={sectionIndex}
              elevation={0}
              sx={{ p: 3, mb: 3, borderRadius: 2, backgroundColor: 'background.paper' }}
            >
              {section.title && (
                <>
                  <Typography variant="h6" gutterBottom>
                    {section.title}
                  </Typography>
                  <Divider sx={{ mb: 3 }} />
                </>
              )}

              <Grid container spacing={3}>
                {section.fields.map((field) => (
                  <Grid
                    item
                    xs={field.gridProps?.xs || 12}
                    sm={field.gridProps?.sm || 6}
                    md={field.gridProps?.md || 4}
                    lg={field.gridProps?.lg || 3}
                    key={field.name}
                  >
                    {renderField(field, formikProps)}
                  </Grid>
                ))}
              </Grid>
            </Paper>
          ))}

          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2, gap: 2 }}>
            {onCancel && (
              <Button
                variant="outlined"
                color="primary"
                onClick={onCancel}
                disabled={loading}
              >
                {cancelButtonText}
              </Button>
            )}
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading || !formikProps.isValid || !formikProps.dirty}
            >
              {loading ? 'Loading...' : submitButtonText}
            </Button>
          </Box>
        </Form>
      )}
    </Formik>
  );
};

export default FormikForm;
