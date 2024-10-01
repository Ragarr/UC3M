//
// Created by ragarr on 11/5/23.
//

#ifndef FLUID_VECTOR3D_HPP
#define FLUID_VECTOR3D_HPP

#include <iostream>
#include <cmath>
#include <array>



template <typename T>
class Vector3D {
  public:
    // getters
    [[nodiscard]] T x() const { return x_; }
    [[nodiscard]] T y() const { return y_; }
    [[nodiscard]] T z() const { return z_; }
    // setters
    void set_x(T x) { x_ = x; }
    void set_y(T y) { y_ = y; }
    void set_z(T z) { z_ = z; }
    Vector3D(T x, T y, T z) : x_(x), y_(y), z_(z) {} // NOLINT // easly swapped values
    Vector3D() = default;

    Vector3D<T> operator+(const Vector3D<T>& other) const {
      return Vector3D<T>(x_ + other.x(), y_ + other.y(), z_ + other.z());
    }
    Vector3D<T> operator-(const Vector3D<T>& other) const {
      return Vector3D<T>(x_ - other.x(), y_ - other.y(), z_ - other.z());
    }
    Vector3D<T> operator*(const Vector3D<T>& other) const {
      return Vector3D<T>(x_ * other.x(), y_ * other.y(), z_ * other.z());
    }
    Vector3D<T> operator*(const T& other) const {
      return Vector3D<T>(x_ * other, y_ * other, z_ * other);
    }
    Vector3D<T> operator/(const Vector3D<T>& other) const {
      return Vector3D<T>(x_ / other.x(), y_ / other.y(), z_ / other.z());
    }
    Vector3D<T> operator/(const T& other) const {
      return Vector3D<T>(x_ / other, y_ / other, z_ / other);
    }
    bool operator==(const Vector3D<T>& other) const {
      return x_ == other.x() && y_ == other.y() && z_ == other.z();
    }

    // convert to int: parte enetra
    [[nodiscard]] Vector3D<int> to_int() const {
      return {(int)(std::floor(x_)), (int)(std::floor(y_)), (int)(std::floor(z_))};
    }

    // convert to double
    [[nodiscard]] Vector3D<double> to_double() const {
            return {(double)x_, (double)y_, (double)z_};
    }
  [[nodiscard]] bool isAdjacent(Vector3D<T> other) const {
      Vector3D<int> const diff = (other - *this).to_int();
      bool const adjacent = (std::abs(diff.x()) == 1 && diff.y() == 0 && diff.z() == 0) ||
                    (diff.x() == 0 && std::abs(diff.y()) == 1 && diff.z() == 0) ||
                    (diff.x() == 0 && diff.y() == 0 && std::abs(diff.z()) == 1) ||
                    (std::abs(diff.x()) == 1 && std::abs(diff.y()) == 1 && diff.z() == 0) ||
                    (std::abs(diff.x()) == 1 && diff.y() == 0 && std::abs(diff.z()) == 1) ||
                    (diff.x() == 0 && std::abs(diff.y()) == 1 && std::abs(diff.z()) == 1) ||
                    (std::abs(diff.x()) == 1 && std::abs(diff.y()) == 1 && std::abs(diff.z()) == 1);
      return adjacent;
  }

  friend std::ostream& operator<<(std::ostream& os, const Vector3D<T>& vector) {
    os << "(" << vector.x_ << ", " << vector.y_ << ", " << vector.z_ << ")";
    return os;
  }

  double norm() {
      return std::sqrt(x_*x_ + y_*y_ + z_*z_);
  }

  private:
    T x_;
    T y_;
    T z_;
};

#endif  // FLUID_VECTOR3D_HPP
