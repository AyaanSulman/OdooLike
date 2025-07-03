import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import {
  TextField,
  Button,
  Typography,
  Box,
  Link,
  InputAdornment,
  IconButton,
  Alert,
  CircularProgress,
  Grid,
  Checkbox,
  FormControlLabel,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { register } from '../../store/slices/authSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';

const validationSchema = Yup.object({
  first_name: Yup.string().required('First name is required'),
  last_name: Yup.string().required('Last name is required'),
  email: Yup.string().email('Enter a valid email').required('Email is required'),
  password: Yup.string()
    .min(8, 'Password should be of minimum 8 characters length')
    .required('Password is required'),
  confirm_password: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Confirm password is required'),
  organization_name: Yup.string().required('Organization name is required'),
  terms_accepted: Yup.boolean().oneOf([true], 'You must accept the terms and conditions'),
});

const Register: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleSubmit = async (values: any) => {
    const { confirm_password, terms_accepted, ...userData } = values;
    await dispatch(register(userData));
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleClickShowConfirmPassword = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto' }}>
      <Typography variant="h5" component="h1" gutterBottom align="center">
        Create an Account
      </Typography>
      <Typography variant="body2" color="textSecondary" align="center" sx={{ mb: 3 }}>
        Fill in the form below to create your account
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Formik
        initialValues={{
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          confirm_password: '',
          organization_name: '',
          terms_accepted: false,
        }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ errors, touched, isValid, dirty }) => (
          <Form>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Field
                  as={TextField}
                  fullWidth
                  id="first_name"
                  name="first_name"
                  label="First Name"
                  variant="outlined"
                  error={touched.first_name && Boolean(errors.first_name)}
                  helperText={touched.first_name && errors.first_name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Field
                  as={TextField}
                  fullWidth
                  id="last_name"
                  name="last_name"
                  label="Last Name"
                  variant="outlined"
                  error={touched.last_name && Boolean(errors.last_name)}
                  helperText={touched.last_name && errors.last_name}
                />
              </Grid>
              <Grid item xs={12}>
                <Field
                  as={TextField}
                  fullWidth
                  id="email"
                  name="email"
                  label="Email Address"
                  variant="outlined"
                  error={touched.email && Boolean(errors.email)}
                  helperText={touched.email && errors.email}
                />
              </Grid>
              <Grid item xs={12}>
                <Field
                  as={TextField}
                  fullWidth
                  id="organization_name"
                  name="organization_name"
                  label="Organization Name"
                  variant="outlined"
                  error={touched.organization_name && Boolean(errors.organization_name)}
                  helperText={touched.organization_name && errors.organization_name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Field
                  as={TextField}
                  fullWidth
                  id="password"
                  name="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  variant="outlined"
                  error={touched.password && Boolean(errors.password)}
                  helperText={touched.password && errors.password}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={handleClickShowPassword}
                          edge="end"
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Field
                  as={TextField}
                  fullWidth
                  id="confirm_password"
                  name="confirm_password"
                  label="Confirm Password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  variant="outlined"
                  error={touched.confirm_password && Boolean(errors.confirm_password)}
                  helperText={touched.confirm_password && errors.confirm_password}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={handleClickShowConfirmPassword}
                          edge="end"
                        >
                          {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <Field
                  as={FormControlLabel}
                  control={<Checkbox color="primary" />}
                  id="terms_accepted"
                  name="terms_accepted"
                  label={
                    <Typography variant="body2">
                      I agree to the{' '}
                      <Link component={RouterLink} to="/terms" variant="body2">
                        Terms and Conditions
                      </Link>
                    </Typography>
                  }
                />
                {touched.terms_accepted && errors.terms_accepted && (
                  <Typography variant="caption" color="error" display="block">
                    {errors.terms_accepted}
                  </Typography>
                )}
              </Grid>
            </Grid>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              size="large"
              disabled={isLoading || !isValid || !dirty}
              sx={{ mt: 3, mb: 2, py: 1.5 }}
            >
              {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Sign Up'}
            </Button>

            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <Typography variant="body2">
                Already have an account?{' '}
                <Link component={RouterLink} to="/login" variant="body2">
                  Sign In
                </Link>
              </Typography>
            </Box>
          </Form>
        )}
      </Formik>
    </Box>
  );
};

export default Register;
